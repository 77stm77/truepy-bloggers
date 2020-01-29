from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from users.models import Account
from users.forms import RegistrationForm, AccountAuthenticationForm, UpdateDescForm
from core.models import Post


def register(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            profile_pic = form.cleaned_data.get("profile_pic")
            account = authenticate(username=username, password=password1)            
            login(request, account)
            return redirect('homepage')
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
    author = Account.objects.get(id=id)
    posts = author.posts.all()
    context = {
        "posts": posts,
        "author" : author,
    }
    return render(request, "my_blog.html", context)

def edit_desc(request, id):
    form = None
    context = {}
    author = get_object_or_404(Account, id=id)

    if request.user != author:
        return redirect('/')

    if request.POST:
        form = UpdateDescForm(request.POST or None, request.FILES or None, instance=author)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            author = obj
            return redirect("my_blog", id=id)

    form = UpdateDescForm(
            initial = {
                "description": author.description,
			}
		)

    context['form'] = form
    return render(request, 'edit-desc.html', context)
