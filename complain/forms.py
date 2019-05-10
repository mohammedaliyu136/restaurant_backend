from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Complain_i
from django import forms


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class ComplainForm(forms.ModelForm):
    class Meta:
        model = Complain_i
        fields = ('title','description', 'document', )