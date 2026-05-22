import re

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from .models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'surname', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'avatar', 'about', 'phone', 'github_url']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone:
            return phone
        if not re.match(r'^(8\d{10}|\+7\d{10})$', phone):
            raise forms.ValidationError(
                'Телефон должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX'
            )
        if phone.startswith('8'):
            phone = '+7' + phone[1:]
        qs = User.objects.filter(phone=phone)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Этот номер уже используется.')
        return phone

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url', '').strip()
        if not url:
            return url

        validate_url = URLValidator()
        try:
            validate_url(url)
        except ValidationError:
            raise forms.ValidationError('Введите корректный URL-адрес.')

        url_lower = url.lower()
        if not (
            url_lower.startswith('https://github.com')
            or url_lower.startswith('http://github.com')
            or url_lower.startswith('https://www.github.com')
            or url_lower.startswith('http://www.github.com')
        ):
            raise forms.ValidationError(
                'Ссылка должна вести именно на GitHub.'
            )

        return url


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Старый пароль'
        self.fields['new_password1'].label = 'Новый пароль'
        self.fields['new_password2'].label = 'Подтвердите пароль'
