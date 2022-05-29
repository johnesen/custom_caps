from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend as BaseModelBackend
# from django.db.models import Q
# from .profile_settings import manager_apps, manager_permissions


UserModel = get_user_model()


class ModelBackend(BaseModelBackend):
    def authenticate(self, request, **kwargs):
        username = kwargs.get(UserModel.USERNAME_FIELD) or kwargs.get('username')
        password = kwargs['password']
        if not username:
            return None
        try:
            # user = UserModel.objects.get(Q(name=username))
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            pass
        else:
            if user.password is not None and user.check_password(password) and self.user_can_authenticate(user):
                return user

    def has_perm(self, user_obj, perm, obj=None):
        return user_obj.is_active

    def has_module_perms(self, user_obj, app_label):
        return user_obj.is_active