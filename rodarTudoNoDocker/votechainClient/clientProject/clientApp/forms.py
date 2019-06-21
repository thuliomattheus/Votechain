from django import forms
from clientProject.clientApp.models import Vote, User, Seeder
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
        self.fields['voterDocument'].label = 'Título de Eleitor'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label

    class Meta:
        model = User
        fields = ('username', 'email', 'voterDocument', 'password1', 'password2')

class VoteForm(forms.ModelForm):

    privateKey = forms.FileField(required=True, label='Private Key')

    def __init__(self, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['candidateRole'].label = 'Cargo do candidato'
        self.fields['candidateNumber'].label = 'Número do candidato'
        self.fields['privateKey'].label = 'Chave privada'
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label

    class Meta:
        model = Vote
        fields = ('candidateRole','candidateNumber', 'privateKey')

class SeederForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SeederForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label

    class Meta:
        model = Seeder
        fields = '__all__'
        exclude = ['user']
