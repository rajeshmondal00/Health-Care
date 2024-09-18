from django.db import models


class Register_User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.TextField(max_length=100)
    dob = models.DateField(max_length=10)
    pincode = models.CharField(max_length=6)
    email = models.EmailField(max_length=50 , primary_key=True,unique=True)
    phone =  models.CharField(max_length=12 ,unique=True)
    password = models.CharField(max_length=12)

# class Appointment(models.Model):
#     department = models.CharField(max_length=30)
#     doctor = models.CharField(max_length=50)
#     name = models.CharField(max_length=50)
#     phone = models.ForeignKey(Register_User,on_delete=models.CASCADE)