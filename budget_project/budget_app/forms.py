from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'username',
            'id':'username',
            'type':'text',
            'placeholder':'Nazwa użytkownika',
            'maxlength': '16',
            'minlength': '6',
            })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'email',
            'id':'email',
            'type':'email',
            'placeholder':'Nazwa budżetu',
            })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'password1',
            'id':'password1',
            'type':'password',
            'placeholder':'Hasło',
            'maxlength':'22',
            'minlength':'8'
            })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'password2',
            'id':'password2',
            'type':'password',
            'placeholder':'Powtórz hasło',
            'maxlength':'22',
            'minlength':'8'
            })
    class Meta:
        model = User
        fields = ('username', 'last_name', 'password1', 'password2')