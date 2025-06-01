from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'telefone', 'cpf', 'cep', 'endereco', 'cidade', 'estado']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'text',
                'id': 'first_name',
                'readonly': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'id': 'email',
                'readonly': True
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'tel',
                'id': 'telefone',
                'pattern': '[0-9]+',
                'inputmode': 'numeric',
                'readonly': True
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'text',
                'id': 'cpf',
                'readonly': True
            }),
            'cep': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'text',
                'id': 'cep',
                'pattern': '[0-9]{8}',
                'maxlength': '8',
                'inputmode': 'numeric',
                'readonly': True
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'text',
                'id': 'endereco',
                'readonly': True
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'text',
                'id': 'cidade',
                'readonly': True
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'id': 'estado',
                'readonly': True
            }),
        }