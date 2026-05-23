import io
import random
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont

from .constants import (
    AVATAR_ANCHOR,
    AVATAR_COLORS,
    AVATAR_FONT_PATH,
    AVATAR_FONT_SIZE,
    AVATAR_SIZE,
    AVATAR_TEXT_COLOR,
    USER_ABOUT_MAX_LENGTH,
    USER_NAME_MAX_LENGTH,
    USER_PHONE_MAX_LENGTH,
    USER_SURNAME_MAX_LENGTH,
)
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Электронная почта', unique=True)
    name = models.CharField(
        verbose_name='Имя', max_length=USER_NAME_MAX_LENGTH
    )
    surname = models.CharField(
        verbose_name='Фамилия', max_length=USER_SURNAME_MAX_LENGTH
    )
    avatar = models.ImageField(verbose_name='Аватар', upload_to='avatars/')
    phone = models.CharField(
        verbose_name='Номер телефона',
        max_length=USER_PHONE_MAX_LENGTH,
        default='',
    )
    github_url = models.URLField(verbose_name='Ссылка на GitHub', blank=True)
    about = models.TextField(
        verbose_name='О себе', max_length=USER_ABOUT_MAX_LENGTH, blank=True
    )
    is_active = models.BooleanField(verbose_name='Активен', default=True)
    is_staff = models.BooleanField(
        verbose_name='Статус персонала', default=False
    )

    favorites = models.ManyToManyField(
        'projects.Project',
        blank=True,
        related_name='interested_users',
        verbose_name='Избранные проекты',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.name} {self.surname}'

    def save(self, *args, **kwargs):
        if not self.pk and not self.avatar:
            self.generate_avatar()
        super().save(*args, **kwargs)

    def generate_avatar(self):
        letter = self.name[0].upper() if self.name else '?'
        color = random.choice(AVATAR_COLORS)
        img = Image.new('RGB', (AVATAR_SIZE, AVATAR_SIZE), color=color)
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype(
                AVATAR_FONT_PATH,
                size=AVATAR_FONT_SIZE,
            )
        except Exception:
            font = ImageFont.load_default()
        bbox = draw.textbbox(AVATAR_ANCHOR, letter, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (AVATAR_SIZE - text_w) // 2 - bbox[0]
        y = (AVATAR_SIZE - text_h) // 2 - bbox[1]
        draw.text((x, y), letter, fill=AVATAR_TEXT_COLOR, font=font)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        filename = f'avatar_{uuid.uuid4()}.png'
        self.avatar.save(filename, ContentFile(buf.getvalue()), save=False)
