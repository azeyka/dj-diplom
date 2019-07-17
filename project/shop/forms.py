from django import forms
from .models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class ReviewForm(forms.Form):
    name = forms.CharField(max_length=20, label='Имя')
    text = forms.CharField(widget=forms.Textarea, label='Отзыв')

    CHOICES = [('1', '1'),
               ('2', '2'),
               ('3', '3'),
               ('4', '4'),
               ('5', '5'),]
    
    stars = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label='')
    
class LoginForm(forms.Form):
    email = forms.CharField(max_length=20, label='E-mail')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    
class SignupForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(), max_length=20, label='E-mail')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    password_repeat = forms.CharField(widget=forms.PasswordInput(), label='Подтвердите пароль')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError('E-mail должен быть в формате example@example.ru!')
        
        try:
            user = User.objects.get(email=email)
            if user:
                raise forms.ValidationError('Пользователь с таким E-mail уже существует!')
        except User.DoesNotExist:
            return email
        
    def clean_password_repeat(self):
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')
        if password != password_repeat:
            raise forms.ValidationError('Пароли не совпадают!')
        
        return password_repeat