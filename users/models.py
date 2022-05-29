from copy import deepcopy

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from customcaps.utils import compress_image 
from caps.models import Caps
from .profile_settings import users_photo_upload_to

class UserManager(BaseUserManager):
    def create_superuser(self, username, password):
        user = self.model(username=username)
        user.set_password(password)
        user.is_superuser = True
        user.is_verified = True
        user.save()
        return user

    def create_user(self, email, password):
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_verified = True
        user.save()
        return user

    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'user'

    USERNAME_FIELD = 'username'

    objects = UserManager()
    username = models.CharField('username', max_length=50, unique=True, help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'), null=True, blank=True)
    phone = PhoneNumberField('Номер телефона', unique=True, null=True, blank=True)
    first_name = models.CharField('Имя', max_length=250, null=True, blank=True)
    last_name = models.CharField('Фамилия', max_length=250, null=True, blank=True)
    email = models.EmailField('Почта(email)', unique=True, null=True, blank=True, validators=(validate_email,))
    photo = models.ImageField('Фото', upload_to=users_photo_upload_to, null=True, blank=True)
    is_verified = models.BooleanField("Польверждение пользователя", default=False)
    is_active = models.BooleanField('Активный', default=True)
    is_superuser = models.BooleanField('Суперпользователь', default=False)
    date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True)
    last_active = models.DateTimeField('Дата последой активосьти', null=True, blank=True)
    favourites = models.ManyToManyField(Caps, verbose_name="Избранные", null=True, blank=True)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.photo_ = deepcopy(self.photo)

    def __str__(self):
        title = self.email or self.phone
        return str(title)

    def save(self, *args, **kwargs):
        if self.photo and self.photo != self.photo_:
            self.photo = compress_image(self.photo, is_medium_thumbnail=True, quality=80)
        super().save(*args, **kwargs)

    @property
    def is_staff(self):
        return self.is_superuser

    def has_module_perms(self, module, *args, **kwargs):
        if not self.is_active:
            return False
        if self.is_superuser:
            return True
        return False

    def has_perm(self, permission, *args, **kwargs):
        if not self.is_active:
            return False
        if self.is_superuser:
            return True
        module, permission = permission.split('.')
        permission = permission.split('_')[0]
        # if permission in manager_permissions.get(module, {}):
        return True
        return False

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"



class Basket(models.Model):
    item = models.ForeignKey(Caps, on_delete=models.CASCADE, related_name='basket_item')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='basket')
    quantity = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.item} - {self.quantity}"

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"