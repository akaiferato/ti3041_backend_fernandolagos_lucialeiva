from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserSignupForm(UserCreationForm):
    birth_date = forms.DateField(
            label="Fecha de nacimiento",
            widget=forms.DateInput(attrs={'type': 'date'}),
            required=False
            )
    phone_number = forms.CharField(
            label="Número de telefono",
            max_length=20,
            required=False
            )
    organization_name = forms.CharField(
            label="Nombre de la organización",
            max_length=20,
            required=True
            )
    organization_rut = forms.CharField(
            label="Rut de la organización",
            max_length=15,
            required=True
            )
    organization_field = forms.CharField(
            label="Área de la organización",
            max_length=20,
            required=False
            )


    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('birth_date', 'phone_number',)
