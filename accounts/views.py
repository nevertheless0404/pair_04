from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

# 회원가입
from accounts.forms import CustomUserCreationForm

# 로그인
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

# 로그아웃
from django.contrib.auth import logout as auth_logout

# 회원정보수정
from accounts.forms import CustomUserChangeForm
from django.contrib.auth.forms import PasswordChangeForm

# 세션 무효화 방지
from django.contrib.auth import update_session_auth_hash

# Create your views here.


def index(request):
    return render(request, "accounts/index.html")


def profile(reqeust, pk):
    profile = get_user_model().objects.get(pk=pk)
    context = {"profile": profile}
    return render(reqeust, "accounts/profile.html", context)


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("accounts:index")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)


def login(request):
    # if request.user.is_authenticated:
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("accounts:index")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "accounts/login.html", context)


def logout(request):
    auth_logout(request)
    return redirect("accounts:index")


def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:index")
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("articles:index")
    else:
        form = PasswordChangeForm(request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/change_password.html", context)


def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect("accouns:index.html")
