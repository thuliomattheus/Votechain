from django import forms
from nodeProject.nodeApp.models import Seeder

class SeederForm(forms.ModelForm):

    class Meta:
        model = Seeder
        fields = '__all__'
        exclude = ['user']
