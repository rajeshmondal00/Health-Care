from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from .models import Register_User
from django.contrib import messages
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
            password = request.POST['password']
            if not Register_User.objects.filter(email=email, phone=phone).exists():
                register_User=Register_User(first_name=first_name,last_name=last_name,address=address,dob=dob,pincode=pincode,email=email,phone=phone,password=password)
                register_User.save()
                messages.success(request, "Profile details updated.")
                return render(request, 'e_verification.html')
            else:
                messages.success(request, "email and phone number alrady used ...")
                return redirect("/register")
    else:
        form = Register_User()
    return render(request,'registration.html' ,{'form': form})
def use_login(request):
    if request.method =="POST":
        email=request.POST["email"]
        password =request.POST["password"]
        user = authenticate(request,email=email, password=password)
        if user is not None:
            messages.success(request, ("please register first...."))
            return redirect("/login")
        else:
            login(request,user)
            return redirect("/")
        
    return render(request,'login.html')
