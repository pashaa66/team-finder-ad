from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from .models import Project


class ProjectForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=[('open', 'Открыт'), ('closed', 'Закрыт')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Статус проекта',
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']
        labels = {
            'name': 'Название проекта',
            'description': 'Описание проекта',
            'github_url': 'Ссылка на GitHub',
        }

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
