from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime
from .models import *
import random
import re


def register(request):
    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if not first_name.isalpha():
            messages.error(request, "Ism faqat harflardan iborat bo‘lishi kerak❗️")
            return render(request, 'account/register.html')

        if not last_name.isalpha():
            messages.error(request, "Familiya faqat harflardan iborat bo‘lishi kerak❗️")
            return render(request, 'account/register.html')

        if len(first_name) < 2 or len(first_name) > 30:
            messages.error(request, "Ism uzunligi 2 dan 30 gacha bo‘lishi kerak❗️")
            return render(request, 'account/register.html')

        if len(last_name) < 2 or len(last_name) > 30:
            messages.error(request, "Familiya uzunligi 2 dan 30 gacha bo‘lishi kerak❗️")
            return render(request, 'account/register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Bu email oldin ro'yxatdan o'tgan❗️")
            return render(request, 'account/register.html')
        else:
            request.session['email'] = email

        if len(password1) < 8:
            messages.error(request, "Parol kamida 8 belgidan iborat bo‘lishi kerak❗️")
            return render(request, 'account/register.html')

        if not re.search(r'[A-Z]', password1):
            messages.error(request, "Parolda kamida bitta katta harf bo‘lishi kerak❗️")
            return render(request, 'account/register.html')

        if not re.search(r'[a-z]', password1):
            messages.error(request, "Parolda kamida bitta kichik harf bo‘lishi kerak❗️")
            return render(request, 'account/register.html')

        if not re.search(r'\d', password1):
            messages.error(request, "Parolda kamida bitta raqam bo‘lishi kerak❗️")
            return render(request, 'account/register.html')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            messages.error(request, "Parolda kamida bitta maxsus belgi bo‘lishi kerak (!@#...)❗️")
            return render(request, 'account/register.html')

        if password1 != password2:
            messages.error(request, "Parollar bir-biriga mos emas❗️")
            return render(request, 'account/register.html')

        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        request.session['email'] = email
        request.session['password'] = password1

        return redirect('register_verify')

    return render(request, 'account/register.html')


def register_verify(request):
    if request.method == 'POST':
        code_entered = request.POST.get('code')
        if code_entered == request.session.get('verification_code'):
            return redirect('register_complete')
        else:
            messages.error(request, 'Kod noto‘g‘ri')
            return redirect('register_verify')

    # Kod yuboriladi
    code = str(random.randint(100000, 999999))
    request.session['verification_code'] = code
    email = request.session.get('email')
    year = datetime.now().year
    # HTML email yuborish
    subject = 'Tasdiqlash kodi'
    from_email = 'noreply@yourdomain.com'
    to_email = [email]
    text_content = f'Sizning tasdiqlash kodingiz: {code}'
    html_content = render_to_string('emails/verification_email.html', {'code': code, 'year': year})

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return render(request, 'account/confirm_email.html')


def resend_code(request):

    email = request.session.get('reset_email')

    if not email:
        messages.error(request, "Email topilmadi yoki siz hali parolni tiklash jarayonini boshlamagansiz❗️")
        return redirect('register')  # bu yerda o‘z sahifangiz nomi bo‘lishi kerak

    # 6 xonali kod yaratish
    code = str(random.randint(100000, 999999))
    request.session['verification_code'] = code

    # Email yuborish
    subject = 'Tasdiqlash kodi (Qayta yuborildi)'
    from_email = 'noreply@yourdomain.com'
    to_email = [email]

    text_content = f'Sizning yangi tasdiqlash kodingiz: {code}'
    html_content = render_to_string('emails/verification_email.html', {'code': code})

    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        messages.success(request, "Yangi tasdiqlash kodi emailingizga yuborildi 📩")
    except Exception as e:
        messages.error(request, f"Email yuborishda xatolik yuz berdi: {str(e)}")

    return render(request, 'account/confirm_email.html')


def register_complete(request):
    email = request.session.get('email')
    first_name = request.session.get('first_name')
    last_name = request.session.get('last_name')
    password = request.session.get('password')

    if not CustomUser.objects.filter(email=email).exists():
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        login(request, user)

    # Sessionni tozalash
    for key in ['email', 'first_name', 'last_name', 'password', 'verification_code']:
        request.session.pop(key, None)

    return render(request, 'account/register_complete.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Muvaffaqiyatli tizimga kirdingiz ✅")
            return redirect('dashboard')  # foydalanuvchi kirgandan keyin yo‘naltiriladigan sahifa
        else:
            messages.error(request, "Email yoki parol noto‘g‘ri ❌")

    return render(request, 'account/login.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        request.session['reset_email'] = email
        user = CustomUser.objects.filter(email=email).first()

        if user:
            code = str(random.randint(100000, 999999))
            request.session['reset_code'] = code
            email = request.session.get('reset_email')
            year = datetime.now().year
            # HTML email yuborish
            subject = 'Tasdiqlash kodi'
            from_email = 'noreply@yourdomain.com'
            to_email = [email]
            text_content = f'Sizning tasdiqlash kodingiz: {code}'
            html_content = render_to_string('emails/verification_email.html', {'code': code, 'year': year})

            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return redirect('verify_code')
        else:
            messages.error(request, "Bunday email mavjud emas.")
    return render(request, 'account/forgot_password.html')


def verify_code(request):
    if request.method == "POST":
        code = request.POST.get("code")
        if code == request.session.get('reset_code'):
            return redirect('reset_password')
        else:
            messages.error(request, "Kod noto‘g‘ri.")
    return render(request, 'account/verify_code.html')


def resend_reset_code(request):
    email = request.session.get('reset_email')

    if not email:
        messages.error(request, "Email topilmadi yoki siz hali parolni tiklash jarayonini boshlamagansiz❗️")
        return redirect('forgot_password')  # bu yerda o‘z sahifangiz nomi bo‘lishi kerak

    # 6 xonali kod yaratish
    code = str(random.randint(100000, 999999))
    request.session['reset_code'] = code

    # Email yuborish
    subject = 'Tasdiqlash kodi (Qayta yuborildi)'
    from_email = 'noreply@yourdomain.com'
    to_email = [email]

    text_content = f'Sizning yangi tasdiqlash kodingiz: {code}'
    html_content = render_to_string('emails/verification_email.html', {'code': code})

    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        messages.success(request, "Yangi tasdiqlash kodi emailingizga yuborildi 📩")
    except Exception as e:
        messages.error(request, f"Email yuborishda xatolik yuz berdi: {str(e)}")

    return render(request, 'account/verify_code.html')


def reset_password(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if len(password1) < 8:
            messages.error(request, "Parol kamida 8 belgidan iborat bo‘lishi kerak❗️")
            return render(request, 'account/password_change.html')

        if not re.search(r'[A-Z]', password1):
            messages.error(request, "Parolda kamida bitta katta harf bo‘lishi kerak❗️")
            return render(request, 'account/password_change.html')

        if not re.search(r'[a-z]', password1):
            messages.error(request, "Parolda kamida bitta kichik harf bo‘lishi kerak❗️")
            return render(request, 'account/password_change.html')

        if not re.search(r'\d', password1):
            messages.error(request, "Parolda kamida bitta raqam bo‘lishi kerak❗️")
            return render(request, 'account/password_change.html')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            messages.error(request, "Parolda kamida bitta maxsus belgi bo‘lishi kerak (!@#...)❗️")
            return render(request, 'account/password_change.html')

        if password1 != password2:
            messages.error(request, "Parollar bir-biriga mos emas❗️")
            return render(request, 'account/password_change.html')

        request.session['reset_password'] = password1
        return redirect('password_changed')
    return render(request, 'account/password_change.html')


def password_changed(request):
    email = request.session.get('reset_email')
    password = request.session.get('reset_password')
    user = CustomUser.objects.filter(email=email).first()

    print(user, email, password)

    user.set_password(password)
    user.save()
    request.session.flush()
    messages.success(request, "Parol yangilandi.")

    return render(request, 'account/password_changed.html')

def log_out(request):
    print(request.user.is_authenticated)  # Foydalanuvchini autentifikatsiyasini tekshirish
    if request.user.is_authenticated:
        logout(request)  # Foydalanuvchini chiqish qilamiz
        return redirect('login')  # Login sahifasiga yo'naltiramiz
    return redirect('login')