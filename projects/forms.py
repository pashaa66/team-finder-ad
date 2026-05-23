from django import forms

from team_finder.mixins import GithubUrlMixin

from .constants import STATUS_CHOICES
from .models import Project


class ProjectForm(GithubUrlMixin, forms.ModelForm):
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']
