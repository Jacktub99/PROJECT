from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

'''
Creo la classe che definisce il form per la registrazione degli utenti,
prendo come modello la classe User già definita da Django che facilita
l'autenticazione degli utenti
Come campi del form imposto l'username (deve essere univoco per ogni utente), l'email,
e due password, dato che voglio che l'utente deve ripeterla due volte quando si registra-
'''
class Signup(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

'''
Il form per il login, invece, ha solo due campi, l'username che è
un campo di testo di massimo 100 caratteri e la password che indico
attraverso il parametro widget che è di tipo password
'''
class Login(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
