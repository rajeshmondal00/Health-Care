from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import login ,logout
from .models import Register_User,Auto_generate,OTP
from .utility import id_generator,password_generator,otp_generate
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .mail import OTP_mail,ID_password_mail
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse_lazy
from .customauth import CustomAuth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# Create your views here.

def home(request):
    # if request.method =="post":
    #         department = request.POST["department"]
    #         doctor = request.POST["doctor"]
    #         name = request.POST["name"]
    #         phone = request.POST["phone"]
            
    return render(request,'index.html')
def index(request):
    return render(request,'index.html')
def profile(request):
    return render(request,'profile.html')

## User registration
def user_register(request):
    if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            gender = request.POST['gender']
            user_type = request.POST['user_type']
            dob = request.POST['dob']
            pincode = request.POST['pincode']
            email = request.POST['email']
            phone = request.POST['phone']
            try: 
                if not User.objects.filter(email=email).exists() or Register_User.objects.filter(phone=phone).exists():
                    auto_generate_id=id_generator()
                    auto_generate_password=password_generator()
                    user = User(username=auto_generate_id,first_name=first_name,last_name=last_name,email=email,password=make_password(auto_generate_password))
                    register_User=Register_User(user=user,address=address,gender=gender,user_type=user_type,dob=dob,pincode=pincode,phone=phone)
                    auto_generate_otp=otp_generate()
                    user.save()
                    if register_User.USER_TYPES == "Staff":
                        staff_group = Group.objects.get(name='Staff_group')
                        user.groups.add(staff_group)
                    elif register_User.USER_TYPES == "Doctor":
                        doctor_group = Group.objects.get(name='Doctor_group')
                        user.groups.add(doctor_group)
                    register_User.save()
                    user_OTP = OTP(user=user,otp=auto_generate_otp,otp_created_at=timezone.now())
                    user_OTP.save()
                    ## send the otp to the user email
                    OTP_mail(auto_generate_otp,email)
                    auto_generate =Auto_generate(user=user,auto_user_id=auto_generate_id,auto_password=make_password(auto_generate_password))
                    messages.success(request, "Profile details updated.")
                    auto_generate.save()                    
                    request.session['user_name'] = user.username  # Save for OTP verification
                    request.session['auto_generate_id'] = auto_generate_id  # Save for OTP verification
                    request.session['auto_generate_password'] = auto_generate_password  # Save for OTP verification
                    return redirect('/verify_otp')

                else:
                    messages.success(request, "email and phone number alrady used ...")
                    return redirect("/register")
                
            except Exception as e:
                    # Code to handle any other exception
                    print("An error occurred:", e)
    else:
        form = Register_User()
    return render(request,'registration.html')

## User login verification
def user_login(request):
    if request.method =="POST":
        user_id=request.POST["user_id"]
        password =request.POST["password"]
        user = CustomAuth.authenticate(request, user_id=user_id, password=password)
        
        if user is not None:
            user.last_login = timezone.now()
            user.save(update_fields=['last_login']) ## save the user login time in the system
            login(request,user)  ## login the user 
            selective_user = Register_User.objects.get(user=user)
            if selective_user.user_type== 4:
                return redirect("/doctor/dashboard") ## redirect Doctor to doctor dashboard page
            elif selective_user.user_type == 3:
                return redirect("/staff/dashboard") ## redirect Staff to staff dashboard page
            else:
                return redirect("/home", {'user': request.user}) ## redirect Petient to home page
        else:
            messages.success(request, "please register first....")
            return redirect("/login")
        
    return render(request,'login.html',{'user': request.user})

## OTP verification
def verify_otp(request):
    user_name = request.session.get("user_name")
    auto_generate_id = request.session.get("auto_generate_id")
    auto_generate_password = request.session.get("auto_generate_password")
    user = User.objects.get(username=user_name)

    if request.method == "POST":
            otp_ins= OTP.objects.filter(user=user).first()
            if not otp_ins :
                messages.error(request, "Invalid or expired OTP.")
            otp = request.POST.get('otp1') + request.POST.get('otp2') + request.POST.get('otp3') + \
              request.POST.get('otp4') + request.POST.get('otp5') + request.POST.get('otp6')
            if otp_ins.is_otp_valid(otp):

                ## send the user ID and User password to the user email
                ID_password_mail(auto_generate_id,auto_generate_password,user.email)
                user.is_active = False
                user.save()
                messages.success(request, "Registration successful! OTP verified.")
                return redirect('/login')
            else:
                messages.error(request, "Invalid or expired OTP.")
    else:
        return render(request, 'otp.html')

## reset password 
def forgot_password(request):
    if request.method == "POST":
        email = request.POST["email"]
        if Auto_generate.objects.filter(email=email).exists():
            user = Auto_generate.objects.get(email=email)
            user_id = user.auto_user_id
            new_password=password_generator()
            user.set_password(new_password)
            user.save()
            ID_password_mail(user_id,new_password,email)
            return redirect("/login")
        else:
            messages.error(request,"Invalid email ID ")
            return redirect("/register")

    return render(request,"forgot_password.html")

 ## logout the user
def user_logout(request):
    logout(request)
    return redirect('/')  # after redirect user go to home page


## staff login 
@login_required
def staff_dashboard(request):
    # Only allow users in the Staff group to view this page
    if request.user.groups.filter(USER_TYPES='Staff').exists():
        return render(request, 'staff_dashboard.html', {})
    else:
        return redirect('/home')  # Redirect non-staff users to home page

## doctor dashboard
def doctor_dashboard(request):
    return render(request, "doctor_dashboard.html",{'user': request.user})

def staff_dashboard(request):
    return render(request, 'staff_dashboard.html', {'user': request.user})
