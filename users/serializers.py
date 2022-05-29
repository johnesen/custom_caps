from caps.models import Caps
from caps.serializers import CapsSerializer
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed

from .models import User, Basket
from . import profile_exceptions
from orders.serializers import OrderSeralizer
from orders.models import Order



class LisrUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'date_joined', 'last_active', 'photo', 'first_name', 'last_name',)
        read_only_fields = ('date_joined', 'last_active')



class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('style', {})
        kwargs['style']['input_type'] = 'password'
        kwargs['write_only'] = True
        super().__init__(*args, **kwargs)


class BasketSerializer(serializers.ModelSerializer):
    # item = CapsSerializer(read_only=True)
    class Meta:
        model = Basket
        fields = ['id', 'item', 'user', 'quantity', 'created_at', 'updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request_user = self.context['request'].user
        if data['user'] == request_user.id:
            return data

class UserSerializer(serializers.ModelSerializer):
    """
        serializer for putput users data to user self
    """
    orders = OrderSeralizer(many=True)
    basket = BasketSerializer(many=True)
    favourites = CapsSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'date_joined', 'last_active', 'photo', 'first_name', 'last_name', 'is_verified', 'favourites', 'basket', 'orders')
        read_only_fields = ('date_joined', 'is_verified', 'last_active')
    


class RegistrationSerializer(serializers.ModelSerializer):
    """
        Serializer for registration user
    """
    password = PasswordField(required=True, allow_blank=False, allow_null=False)
    password2 = PasswordField(required=True, allow_blank=False, allow_null=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'password2', 'first_name', 'last_name', 'phone',]

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        account = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            phone=self.validated_data['phone'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Password must much'}
            )
        account.set_password(password)
        account.save()
        return account


class LoginResponseSerializer(serializers.Serializer):
    """
        Serializer for output after login user
    """
    user = UserSerializer()
    refresh = serializers.CharField()
    access = serializers.CharField()

# class EmailVerificationSerializer(serializers.ModelSerializer):
#     """
#         Serializer for email verufication
#     """
#     token = serializers.CharField(max_length=555)

#     class Meta:
#         model = User
#         fields = ['token']


class LoginSerializer(serializers.Serializer):
    """
        Serializer for login user
    """
    username = serializers.CharField(max_length=50, required=True, allow_blank=False, allow_null=False)
    password = PasswordField(required=True, allow_blank=False, allow_null=False)

class UpdatePasswordSerializer(serializers.Serializer):
    """
        Serializer for update user passoword
    """
    old_password = PasswordField(required=True)
    new_password = PasswordField(required=True)

    def validate_old_password(self, value):
        if self.context['request'].user.password is None:
            raise profile_exceptions.ValidationError('your account do not have a password set up')
        if not self.context['request'].user.check_password(value):
            raise profile_exceptions.ValidationError('incorrect password')
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

class LogOutRefreshTokenSerializer(serializers.Serializer):
    """
        Serializer for refresh toekn
    """
    refresh = serializers.CharField()

    default_error_messages = {'bad_token': ('Token is invalid or expired')}

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    class Meta:
        fields = ['email']

class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=64, write_only=True)
    token = serializers.CharField(min_length=8, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
