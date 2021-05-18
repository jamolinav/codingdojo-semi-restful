from django.forms import ModelForm, PasswordInput, TextInput
from ...models import Shows

class ShowForm(ModelForm):
    class Meta:
        model = Shows
        fields = '__all__'
        #fields = ['name']
        widgets = {
            #'name' : PasswordInput,
            'title' : TextInput(attrs={'placeholder': '<Título>', 'class': 'inputForm'}),
            'release_date' : TextInput(attrs={'type': 'date', 'class': 'inputForm'}),
        }
        labels = {
            'title'  : 'Título'
        }