from django.forms import ModelForm, PasswordInput, TextInput
from django import forms
from ..models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        #fields = ['name']
        widgets = {
            'password' : PasswordInput,
            'first_name' : TextInput(attrs={'placeholder': '<nombres>'}),
            'last_name' : TextInput(attrs={'placeholder': '<apellidos>'}),
        }
        labels = {
            'first_name'  : 'Nombres',
            'last_name'  : 'Apellidos'
        }

class UserLoginForm(forms.Form):
    email       = forms.EmailField(max_length=100, required=True)
    password    = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        email       = self.cleaned_data.get('email')
        password    = self.cleaned_data.get('password')
        user        = User.authenticate(email, password)
        if not user:
            raise forms.ValidationError("Lo sentimos, login fallido, vuelva a intentar")
        return self.cleaned_data

    def login(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user        = User.authenticate(email, password)
        return user