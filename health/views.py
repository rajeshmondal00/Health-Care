from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from .models import Register_User,Auto_generate
from .utility import id_generator,password_generator
from django.contrib import messages
from django.core.mail import send_mail
from Health_Care.settings import EMAIL_HOST_USER
from django.contrib.auth.hashers import make_password
# Create your views here.

def home(request):
    # if request.method =="post":
    #         department = request.POST["department"]
    #         doctor = request.POST["doctor"]
    #         name = request.POST["name"]
    #         phone = request.POST["phone"]
            
    return render(request,'home.html')
def index(request):
    return render(request,'index.html')
def profile(request):
    return render(request,'profile.html')
def use_register(request):
    if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            dob = request.POST['dob']
            pincode = request.POST['pincode']
            email = request.POST['email']
            phone = request.POST['phone']
            if not Register_User.objects.filter(email=email, phone=phone).exists():
                register_User=Register_User(first_name=first_name,last_name=last_name,address=address,dob=dob,pincode=pincode,email=email,phone=phone)
                auto_generate_id=id_generator()
                auto_generate_password=password_generator()
                try:
                    auto_generate =Auto_generate(email=register_User,auto_user_id=auto_generate_id,auto_password=make_password(auto_generate_password))
                    register_User.save()
                    messages.success(request, "Profile details updated.")
                    auto_generate.save()
                    send_mail(
                                subject="Your ID Code and Password : ",
                                message=f"Your ID is :  {auto_generate_id} \n\n\n Password : {auto_generate_password}",
                                from_email=EMAIL_HOST_USER,
                                recipient_list=[email],
                                fail_silently=False
                             )

                    return render(request,"e_verification.html")
                except Exception as e:
                    # Code to handle any other exception
                    print("An error occurred:", e)
            else:
                messages.success(request, "email and phone number alrady used ...")
                return redirect("/register")
    else:
        form = Register_User()
    return render(request,'registration.html')
def use_login(request):
    if request.method =="POST":
        user_id=request.POST["user_id"]
        password =request.POST["password"]
        user = authenticate(request,user_id=user_id, password=password)
        if user is not None:
            messages.success(request, ("please register first...."))
            return redirect("/login")
        else:
            login(request,user)
            return redirect("/")
        
    return render(request,'login.html')

def otp(request):
    return render(request, "otp.html")