from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from users.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=30, help_text="Для регистрации нужен ваш адресс электронной почты")

    class Meta:
        model = Account
        fields = ("email", "username", "password1", "password2", "profile_pic")

class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("username", "password")

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data["password"]
        if not authenticate(username=username, password=password):
            raise forms.ValidationError("Неправильный логин")
