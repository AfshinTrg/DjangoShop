from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm
from django.contrib import messages
import random
from .utils import send_otp_code_phone, send_otp_code_email
from .models import OtpCode


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
                send_otp_code_phone(cd['phone'], random_code)
            OtpCode.objects.create(email=cd['email'], phone_number=cd['phone'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': cd['phone'],
                'email': cd['email'],
                'full_name': cd['full_name'],
                'password': cd['password1']
            }
            messages.success(request, 'we sent you a code', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})


class UserRegisterVerifyCodeView(View):
    pass


