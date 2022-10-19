from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, VerifyCodeForm
from django.contrib import messages
import random
from .utils import send_otp_code_phone, send_otp_code_email
from datetime import datetime, timedelta
from .models import OtpCode, User


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/UserRegister.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_code = random.randint(1000, 9999)
            if cd['otp_way'] == 'e':
                send_otp_code_email(cd['email'], random_code)
            elif cd['otp_way'] == 'p':
                send_otp_code_phone(cd['phone_number'], random_code)
            OtpCode.objects.create(email=cd['email'], phone_number=cd['phone_number'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': cd['phone_number'],
                'email': cd['email'],
                'username': cd['username'],
                'password': cd['password1']
            }
            messages.success(request, 'we sent you a code', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm
    template_name = 'accounts/Verify.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        expired_time = code_instance.created + timedelta(minutes=1)
        form = self.form_class(request.POST)
        if expired_time > datetime.now():
            if form.is_valid():
                cd = form.cleaned_data
                if cd['code'] == code_instance.code:
                    print(user_session)
                    User.objects.create_user(**user_session)
                    code_instance.delete()
                    messages.success(request, 'you registered', 'success')
                    return redirect('home:home')
                else:
                    messages.error(request, 'this code is wrong', 'danger')
                    return redirect('accounts:verify_code')
            return redirect('home:home')
        else:
            code_instance.delete()
            messages.error(request, 'Your time expired, please try again', 'danger')
            return redirect('accounts:user_register')


