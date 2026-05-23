from django.conf import settings
from django.db import models
from django.urls import reverse

from .constants import (
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_STATUS_MAX_LENGTH,
    STATUS_CHOICES,
    STATUS_OPEN,
)


class Project(models.Model):
    name = models.CharField(
        verbose_name='Название проекта', max_length=PROJECT_NAME_MAX_LENGTH
    )
    description = models.TextField(verbose_name='Описание проекта', blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name='Владелец',
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания', auto_now_add=True
    )
    github_url = models.URLField(verbose_name='Ссылка на GitHub', blank=True)
    status = models.CharField(
        verbose_name='Статус',
        max_length=PROJECT_STATUS_MAX_LENGTH,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='participated_projects',
        verbose_name='Участники',
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'project_id': self.pk})
