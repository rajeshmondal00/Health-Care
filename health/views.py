from django.utils import timezone
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from .models import Register_User,Auto_generate,OTP
from .utility import id_generator,password_generator,otp_generate
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .mail import OTP_mail,ID_password_mail
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
                auto_generate_otp=otp_generate()
                register_User.save()
                user_OTP = OTP(email=register_User,otp=auto_generate_otp,otp_created_at=timezone.now())
                user_OTP.save()
                try:
                    ## send the otp to the user email
                    OTP_mail(auto_generate_otp,email)
                    auto_generate =Auto_generate(email=register_User,auto_user_id=auto_generate_id,auto_password=make_password(auto_generate_password))
                    register_User.is_active= False
                    messages.success(request, "Profile details updated.")
                    auto_generate.save()

                    request.session['email'] = register_User.email  # Save for OTP verification
                    request.session['auto_generate_id'] = auto_generate_id  # Save for OTP verification
                    request.session['auto_generate_password'] = auto_generate_password  # Save for OTP verification
                    return redirect('/verify_otp')
                
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

def verify_otp(request):
    email = request.session.get("email")
    auto_generate_id = request.session.get("auto_generate_id")
    auto_generate_password = request.session.get("auto_generate_password")
    user = Register_User.objects.get(email=email)

    if request.method == "POST":
            otp_ins= OTP.objects.filter(email=user).first()
            if not otp_ins :
                messages.error(request, "Invalid or expired OTP.")
            otp = request.POST.get('otp1') + request.POST.get('otp2') + request.POST.get('otp3') + \
              request.POST.get('otp4') + request.POST.get('otp5') + request.POST.get('otp6')
            if otp_ins.is_otp_valid(otp):

                ## send the user ID and User password to the user email
                ID_password_mail(auto_generate_id,auto_generate_password,email)
                user.is_active = True
                user.save()
                messages.success(request, "Registration successful! OTP verified.")
                return redirect('/login')
            else:
                messages.error(request, "Invalid or expired OTP.")
    else:
        return render(request, 'otp.html')


def forgot_password(request):
    if request.method == "POST":
        email = request.POST["email"]
        if Auto_generate.objects.filter(email=email).exists():
            user = Auto_generate.objects.get(email=email)
            user_id = user.auto_user_id
            auto_generate_password=password_generator()
            user.auto_user_password = auto_generate_password
            user.save()
            ID_password_mail(user_id,auto_generate_password,email)
            return redirect("/login")
        else:
            messages.error(request,"Invalid email ID ")
            return redirect("/register")

    return render(request,"forgot_password.html")

