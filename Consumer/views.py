from allauth.account.views import LoginView
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       UserCreationForm)
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render


# Create your views here.
def home(request):
    blogs=Blog.objects.all()
    print(blogs)
    return render(request, "home.html", {"data": blogs})


def signupuser(request):
    if request.method == "POST":
        fm = request.POST
        rem=request.POST.get('remeber',False)
        uname=request.POST.get('username')
        print(rem)
        um = fm["username"]
        pw = fm["password1"]
        pw2 = fm["password2"]
        email=fm['email']
        if not rem:
            request.session.set_expiry(0)   
        if pw != pw2:
            return render(
                request,
                "signup.html",
                {"form": UserCreationForm(), "error": "Password doesnt match"},
            )
        else:
            try:
                user = User.objects.create_user(um, password=pw,email=email)
                user.save()
                login(request, user)
                return redirect("/")
            except IntegrityError:
                return render(
                    request,
                    "allauth/account/signup.html",
                    {"form": UserCreationForm(), "error": "Username already exists"},
                )
    else:
        return render(request, "signup.html", {"form": UserCreationForm})


def loginuser(request):
    if request.method == "POST":
        fm = request.POST
        print(fm)
        user = authenticate(request, username=fm["username"], password=fm["password"])

        if user is None:
            return render(
                request,
                "login.html",
                {
                    "form": AuthenticationForm(),
                    "error": "User not found. Invalid crendentials",
                },
            )
        else:
            login(request, user)
            return redirect("/")
    else:
        return render(request, "allauth/account/login.html", {"form": AuthenticationForm()})


def logoutuser(request):
    logout(request)
    return redirect("/")

def changepassword(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = request.user
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)  # Set the new password
            user.save()
            update_session_auth_hash(request, user)  # Update the session to avoid logout
            return redirect("/")
        else:
            return render(
                request,
                "changepassword.html",
                {"form": form, "error": "New Password doesn't match"},
            )
    else:
        form = PasswordChangeForm(request.user)
        return render(request, "changepassword.html", {"form": form})
    
def error404(request,exception):
    return render(request,"error404.html",{"exception",exception},status=404)


def redirecthome(request):
    print("hi")
    return redirect('home')

class CustomLoginView(LoginView):
    template_name = 'signup.html'
