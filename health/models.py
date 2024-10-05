from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

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

class OTP(models.Model):
    email =  models.ForeignKey(Register_User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    def is_otp_valid(self, otp):
        time_diff = timezone.now() - self.otp_created_at
        return self.otp == otp and time_diff.total_seconds() < 300  # 5 minutes validity
