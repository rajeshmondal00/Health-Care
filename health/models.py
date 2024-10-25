from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils import timezone

## user registration
class Register_User(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    address = models.TextField(max_length=100)
    dob = models.DateField(max_length=10)
    pincode = models.CharField(max_length=6)
    phone =  models.CharField(max_length=12 ,unique=True)
    is_active = models.BooleanField(default=False)
    GENDER_CHOICES = (('male', 'Male'),
                      ('female', 'Female'),
                      ('other', 'Other'),)
    
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    USER_TYPES = ((2, 'Patient'),
                  (3, 'Staff'),
                  (4, 'Doctor'),) 
    user_type = models.IntegerField(choices=USER_TYPES)

    class Meta:
        db_table="health_register_user"


# class Appointment(models.Model):
#     department = models.CharField(max_length=30)
#     doctor = models.CharField(max_length=50)
#     name = models.CharField(max_length=50)
#     phone = models.ForeignKey(Register_User,on_delete=models.CASCADE)

## generate auto user id and password
class Auto_generate(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    auto_user_id = models.CharField(max_length=12)
    auto_password = models.CharField(max_length=255)
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table="health_auto_generate"
    

class OTP(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    def is_otp_valid(self, otp):
        time_diff = timezone.now() - self.otp_created_at
        return self.otp == otp and time_diff.total_seconds() < 300  # 5 minutes validity
    
    class Meta:
        db_table="health_otp"
    