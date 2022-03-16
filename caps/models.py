from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, User
from datetime import datetime

from baner.models import Baner

class Brand(models.Model):
    """категория и названия брендов"""
    name = models.CharField("Бренд", max_length=50)
    icon = models.FileField("Иконка бренда", upload_to='brand_icon/')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
         return self.name

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"


class Sizes(models.Model):
    """размеры"""
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
    """
        товар(кепки)
    """
    brand = models.ForeignKey(Brand, verbose_name="Имя бренда", on_delete=models.CASCADE, null=True)
    name = models.CharField("Названия", max_length=250)
    price = models.IntegerField()
    size = models.ManyToManyField(Sizes, verbose_name="Размер", related_name='sizes')
    description = models.TextField("Описания")
    is_available = models.BooleanField(default=True, verbose_name="в Наличии")
    available = AvailableManager()
    new_price = models.IntegerField(null=True, blank=True)
    in_baner = models.ForeignKey(Baner, null=True, blank=True, on_delete=models.SET_NULL, related_name='caps')

    created_data = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Кепка"
        verbose_name_plural = "Кепки"


class UserCapsFavorite(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name='favourites')
    caps = models.ForeignKey(Caps, verbose_name="Кепки", on_delete=models.CASCADE)
    is_favorite = models.BooleanField("Избранные", default=True)

    class Meta:
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'

    # def __str__(self):
    #     return f'{self.caps}, {self.user.username}'


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(Caps, on_delete=models.CASCADE, null=True, blank=True)
    size = models.ForeignKey(Sizes, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.user,
                                               self.item,
                                               self.quantity,
                                               self.created_at,
                                               self.updated_at)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"


class CapsImage(models.Model):
    """Фотки с кепками"""
    image = models.ImageField("Изображение", upload_to="caps_foto/")
    caps = models.ForeignKey(Caps, verbose_name="Кепки", on_delete=models.CASCADE, related_name="capsimage")

    def __str__(self):
        return f'{self.caps}'

    class Meta:
        verbose_name = "Фотографии кепок"
        verbose_name_plural = "Фотографии кепок"
