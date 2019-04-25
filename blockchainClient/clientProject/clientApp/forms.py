from django import forms
from clientProject.clientApp.models import Vote, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label

class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['email'].required = True
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label

    class Meta:
        model = User
        fields = ('username', 'email', 'cpf', 'password1', 'password2')

class VoteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label

    class Meta:
        model = Vote
        fields = ('candidateRole','candidateNumber')