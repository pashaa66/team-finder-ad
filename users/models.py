import io
import random
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont

AVATAR_COLORS = [
    '#4F6D7A',
    '#5B8DB8',
    '#6BAA75',
    '#7B6D8D',
    '#8B635A',
    '#6B8E6B',
    '#7A7FAD',
    '#9A7D6B',
    '#5C7A6B',
    '#7A5C8B',
]


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(
            email=email, name=name, surname=surname, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, name, surname, password=None, **extra_fields
    ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, surname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    avatar = models.ImageField(upload_to='avatars/')
    phone = models.CharField(max_length=12, default='')
    github_url = models.URLField(blank=True)
    about = models.TextField(max_length=256, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    def __str__(self):
        return f'{self.name} {self.surname}'

    def generate_avatar(self):
        letter = self.name[0].upper() if self.name else '?'
        color = random.choice(AVATAR_COLORS)
        size = 200
        img = Image.new('RGB', (size, size), color=color)
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype(
                '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                size=100,
            )
        except Exception:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), letter, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (size - text_w) // 2 - bbox[0]
        y = (size - text_h) // 2 - bbox[1]
        draw.text((x, y), letter, fill='white', font=font)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        filename = f'avatar_{uuid.uuid4()}.png'
        self.avatar.save(filename, ContentFile(buf.getvalue()), save=False)

    def save(self, *args, **kwargs):
        if not self.pk and not self.avatar:
            self.generate_avatar()
        super().save(*args, **kwargs)
