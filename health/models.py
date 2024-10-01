from django.db import models
from django.contrib.auth.hashers import make_password

## user registration
class Register_User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.TextField(max_length=100)
    dob = models.DateField(max_length=10)
    pincode = models.CharField(max_length=6)
    email = models.EmailField(max_length=50 , primary_key=True,unique=True)
    phone =  models.CharField(max_length=12 ,unique=True)


# class Appointment(models.Model):
#     department = models.CharField(max_length=30)
#     doctor = models.CharField(max_length=50)
#     name = models.CharField(max_length=50)
#     phone = models.ForeignKey(Register_User,on_delete=models.CASCADE)

## generate auto user id and password
class Auto_generate(models.Model):
    email =  models.ForeignKey(Register_User, on_delete=models.CASCADE)
    auto_user_id = models.CharField(max_length=12)
    auto_password = models.CharField(max_length=255)

    def save(self,*args,**kwargs):
        ## password convert and save into hashed format
        self.auto_password = make_password(self.auto_password)
        super(Auto_generate, self).save(*args, **kwargs)

# from django.utils import timezone
# from datetime import timedelta
    # def is_valid(self):
    #     return timezone.now() < self.created_at + timedelta(minutes=10)  # OTP valid for 10 minutes


## otp generate models
# from django_otp.models import OTPBase

# class CustomOTP(OTPBase):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)