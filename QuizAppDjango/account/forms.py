from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
           attrs = { 'placeholder': 'Passwort einfuegen'}), help_text='Passwort')
    username = forms.CharField(widget=forms.TextInput(
           attrs = { 'placeholder': 'Benutzername einfuegen'}), help_text='Accountname')
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Name einfuegen'}), help_text='Name')
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Email einfuegen'}), help_text='E-Mail')

    class Meta:
        model = User
        fields = ['username', 'last_name', 'email', 'password']


class PictureForm(forms.Form):
    picture = forms.FileField()
    rank = forms.IntegerField()
