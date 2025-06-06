from django.shortcuts import render,redirect
from django.contrib import messages
import urllib.request
import urllib.parse
from django.contrib.auth import logout
from django.core.mail import send_mail
import os
import random
from django.conf import settings
from baseapp.models import *



# Create your views here.




EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')



def sendSMS(user, otp, mobile):
    data = urllib.parse.urlencode(
        {
            "username": "Codebook",
            "apikey": "56dbbdc9cea86b276f6c",
            "mobile": mobile,
            "message": f"Hello {user}, your OTP for account activation is {otp}. This message is generated from https://www.codebook.in server. Thank you",
            "senderid": "CODEBK",
        }
    )
    data = data.encode("utf-8")
    request = urllib.request.Request("https://smslogin.co/v3/api.php?")
    f = urllib.request.urlopen(request, data)
    return f.read()


def generate_otp(length=4):
    otp = "".join(random.choices("0123456789", k=length))
    return otp


def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('name')
        password = request.POST.get('password')
        if username == 'admin' and password == 'admin':
            messages.success(request, 'Login Successful')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid details !')
            return redirect('admin_login')
    return render(request, "admin_login.html")



def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = User.objects.get(email=email)
            if user.password != password:
                messages.error(request, "Incorrect password.")
                return redirect("user_login")
            if user.status == "Accepted":
                if user.otp_status == "Verified":
                    request.session["user_id_after_login"] = user.pk
                    messages.success(request, "Login successful!")
                    return redirect("user_dashboard")
                else:
                    new_otp = generate_otp()
                    user.otp = new_otp
                    user.otp_status = "Not Verified"
                    user.save()
                    subject = "New OTP for Verification"
                    message = f"Your new OTP for verification is: {new_otp}"
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [user.email]
                    send_mail(
                        subject, message, from_email, recipient_list, fail_silently=False
                    )
                    sendSMS(user.full_name, new_otp, user.phone_number)
                    messages.warning(
                        request,
                        "OTP not verified. A new OTP has been sent to your email and phone.",
                    )
                    request.session["id_for_otp_verification_user"] = user.pk
                    return redirect("user_otp")
            else:
                if user.status == "Hold":
                    messages.error(request, "Your account is temporarily on hold for posting prohibited content. Please contact the admin for more details.")
                    return redirect("user_login")
                else:
                    messages.info(request, "Your Account is Not Accepted by Admin Yet")
                    return redirect("user_login")
        except User.DoesNotExist:
            messages.error(request, "Email not registered.")
            return redirect("user_login")
    return render(request, "user_login.html")



def user_register(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password') 
        phone_number = request.POST.get('phone_number')
        age = request.POST.get('age')
        address = request.POST.get('address')
        photo = request.FILES.get('photo')
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect('user_register')
        user = User(
            full_name=full_name,
            email=email,
            password=password, 
            phone_number=phone_number,
            age=age,
            address=address,
            photo=photo
        )
        user.save()
        otp = generate_otp()
        user.otp = otp
        user.save()
        subject = "OTP Verification for Account Activation"
        message = f"Hello {full_name},\n\nYour OTP for account activation is: {otp}\n\nIf you did not request this OTP, please ignore this email."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        request.session["id_for_otp_verification_user"] = user.pk
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        if sendSMS:
            sendSMS(full_name, otp, phone_number)
        messages.success(request, "OTP has been sent to your email and phone number!")
        return redirect("user_otp")
    return render(request, "user_register.html")


def contact(request):
    return render(request, "contact.html")



def user_otp(request):
    otp_user_id = request.session.get("id_for_otp_verification_user")
    if not otp_user_id:
        messages.error(request, "No OTP session found. Please try again.")
        return redirect("user_register")
    if request.method == "POST":
        entered_otp = "".join(
            [
                request.POST["first"],
                request.POST["second"],
                request.POST["third"],
                request.POST["fourth"],
            ]
        )
        try:
            user = User.objects.get(id=otp_user_id)
        except User.DoesNotExist:
            messages.error(request, "User not found. Please try again.")
            return redirect("user_register")
        if user.otp == entered_otp:
            user.otp_status = "Verified"
            user.save()
            messages.success(request, "OTP verification successful!")
            return redirect("user_login")
        else:
            messages.error(request, "Incorrect OTP. Please try again.")
            return redirect("user_otp")
    return render(request, "user_otp.html")

