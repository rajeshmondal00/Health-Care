from django.core.mail import send_mail
from Health_Care.settings import EMAIL_HOST_USER

## send the otp to the user email
def OTP_mail(auto_generate_otp,email):
    send_mail(
            subject="Your OTP : ",
            message=f" {auto_generate_otp} \n\n\n Please don't share with anyone . ",
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
            )
    
## send the user ID and User password to the user email
def ID_password_mail(auto_generate_id,auto_generate_password,email):
    send_mail(
            subject="Your ID Code and Password : ",
            message=f"Your ID is :  {auto_generate_id} \n\n\n Password : {auto_generate_password}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
            )