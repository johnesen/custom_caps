from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, User
from customcaps.utils import get_filename, compress_image
import os
from copy import deepcopy

from baner.models import Baner

class Brand(models.Model):
    name = models.CharField("Бренд", max_length=50)
    icon = models.FileField("Иконка бренда", upload_to='brand_icon/')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
         return self.name

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"


class Sizes(models.Model):
    value = models.CharField("Значение", max_length=2)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Размеры"
        verbose_name_plural = "Размеры"


class AvailableManager(models.Manager):
    def get_queryset(self):
        return super(AvailableManager, self).get_queryset().filter(is_available=True)

class Caps(models.Model):
    brand = models.ForeignKey(Brand, verbose_name="Имя бренда", on_delete=models.CASCADE, null=True)
    name = models.CharField("Названия", max_length=250)
    price = models.IntegerField("цена")
    size = models.ManyToManyField(Sizes, verbose_name="Размер", related_name='sizes')
    description = models.TextField("Описания")
    is_available = models.BooleanField(default=True, verbose_name="в Наличии")
    available = AvailableManager()
    new_price = models.IntegerField(null=True, blank=True)
    created_data = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Кепка"
        verbose_name_plural = "Кепки"


USERS_UPLOAD_DIR = 'user/photo'

def users_photo_upload_to(instance, filename):
    new_filename = get_filename(filename)
    return os.path.join(USERS_UPLOAD_DIR, new_filename)


class CapsImage(models.Model):
    photo = models.ImageField("Изображение", upload_to=users_photo_upload_to)
    caps = models.ForeignKey(Caps, verbose_name="Кепки", on_delete=models.CASCADE, related_name="capsimage")

    def __str__(self):
        return f'{self.caps}'

    class Meta:
        verbose_name = "Фотографии кепок"
        verbose_name_plural = "Фотографии кепок"


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.photo_ = deepcopy(self.photo)

    def save(self, *args, **kwargs):
        if self.photo and self.photo != self.photo_:
            self.photo = compress_image(self.photo, is_medium_thumbnail=True, quality=80)
        super().save(*args, **kwargs)
