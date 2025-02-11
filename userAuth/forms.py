from django import forms
from django.contrib.auth.forms import UserCreationForm
# from phonenumber_field.formfields import PhoneNumberField
from userAuth.models import CustomUser
from django.core.validators import RegexValidator



class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Nom"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Numeros de telephone"}))  # Champ de numéro de téléphone
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Mot de Pass"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Mot de Pass"}))
    country = forms.CharField(widget=forms.HiddenInput())
    

    class Meta:
        model = CustomUser
        fields = ['username', 'email','phone_number','country']



class CodeSecretForm(forms.Form):
    code_secret = forms.CharField(
         widget=forms.PasswordInput(attrs={
              'placeholder': 'Veuiller saisir un code secret', 
              }), 
              max_length=5,
              min_length=5,
              required=True,
              validators=[RegexValidator(r'^\d{5}$', 'Veuillez saisir exactement 5 chiffres')],
              )

    class Meta:
        model = CustomUser
        fields = ['secret_code']
