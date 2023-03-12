from django import forms
from django.contrib.auth.models import User
from .models import Profile


class FormLogin(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={"type": "text", "class": "sign__input",
                                                           "placeholder": "Email"}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={"type": "password", "class": "sign__input",
                                                                 "placeholder": "Password"}))


class FormRegistration(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"type": "password", "class": "sign__input",
                                                                  "placeholder": "Repeat your Password"}))

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password')

        widgets = {
            'first_name': forms.TextInput(attrs={"type": "text", "class": "sign__input", "placeholder": "Username"}),
            'email': forms.EmailInput(attrs={"type": "text", "class": "sign__input", "placeholder": "Email"}),
            'password': forms.PasswordInput(attrs={"type": "password", "class": "sign__input", "placeholder": "Password"}),
        }


class FormUpdateUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'email')

        widgets = {
            'first_name': forms.TextInput(attrs={'id': 'username', "type": 'text', 'class': 'profile__input',
                                                 'placeholder': 'first name'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'type': 'text', 'class': 'profile__input',
                                             'placeholder': 'email@email.com'}),
        }


class FormUpdateProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('last_name', 'phone_number')
        widgets = {
            'last_name': forms.TextInput(attrs={'id': 'firstname', 'type': 'text', 'class': 'profile__input',
                                                'placeholder': 'last name'}),
            'phone_number': forms.EmailInput(attrs={'id': 'lastname', 'type': 'text', 'class': 'profile__input',
                                                    'placeholder': 'phone_number'}),
        }


class FormUpdateAvatar(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_img']


class FormChangePassword(forms.Form):

    passwordOld = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'oldpass', 'type': 'password',
                                                                    'name': 'old_pass', 'class': 'profile__input'}))

    passwordNew = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'newpass', 'type': 'password',
                                                                    'name': 'new_pass', 'class': 'profile__input'}))

    passwordConf = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'confirmpass', 'type': 'password',
                                                                     'name': 'confirm_pass', 'class': 'profile__input'}))





