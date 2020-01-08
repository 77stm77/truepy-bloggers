from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from users.models import Account
from users.forms import RegistrationForm, AccountAuthenticationForm


def register(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=password1)
            profile_pic = form.cleaned_data.get("profile_pic")
            login(request, account)
            return redirect('home')
        else:
            context["registration_form"] = form
    else:
        form = RegistrationForm()
        context["registration_form"] = form
    return render(request, "register.html", context)


def logout_view(request):
	logout(request)
	return redirect('/')

def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("homepage")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("homepage")

    else:
        form = AccountAuthenticationForm()

    context["login"] = form
    return render(request, "login.html", context)

def must_authenticate_view(request):
	return render(request, 'must_auth.html', {})


def my_blog(request, id):
    accounts = Account.objects.filter(id=id)
    posts = accounts.posts
    context = {
        "posts": posts
    }
    return render(request, "my_blog.html", context)
