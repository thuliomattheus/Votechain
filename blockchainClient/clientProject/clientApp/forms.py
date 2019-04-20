from django import forms
from clientProject.clientApp.models import Vote, User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('cpf', 'password')

class RegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = None

    class Meta:
        model = User
        fields = ('username', 'email', 'cpf', 'password1', 'password2')
