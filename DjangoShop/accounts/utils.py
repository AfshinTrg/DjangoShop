from kavenegar import *
from decouple import config
from django.conf import settings
from django.core.mail import send_mail


def send_otp_code_phone(phone_number, code):
    try:
        api = KavenegarAPI(config('API_NAME'))
        params = {
            'sender': '',
            'receptor': phone_number,
            'message': f'{code} کد تایید شما '
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def send_otp_code_email(email, code):
    subject = 'Thank you for registering to our site'
    message = f'Thank you for registering to our site, Your code is : {code}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)
