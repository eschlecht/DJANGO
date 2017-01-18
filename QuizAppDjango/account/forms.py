from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
           attrs = { 'placeholder': 'Passwort einfuegen'}) )
    username = forms.CharField(widget=forms.TextInput(
           attrs = { 'placeholder': 'Benutzername einfuegen'}) )
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Name einfuegen'}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Email einfuegen'}))

    class Meta:
        model = User
        fields = ['username', 'last_name', 'email', 'password']


class PictureForm(forms.Form):
    picture = forms.FileField()
    rank = forms.IntegerField()
