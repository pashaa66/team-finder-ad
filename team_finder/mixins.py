from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


class GithubUrlMixin:
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
