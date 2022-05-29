import jwt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import response, mixins, viewsets, exceptions, generics, status, views

from django.contrib.auth import login as log, authenticate 
from rest_framework.views import APIView
from customcaps import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site

from users.profile_settings import HOST_OF_SERVER

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse



from .models import Basket, User
from .utils import Util
from .serializers import (
    BasketSerializer,
    # EmailVerificationSerializer,
    LoginSerializer,
    RegistrationSerializer,
    LogOutRefreshTokenSerializer,
    ResetPasswordEmailRequestSerializer,
    ResetPasswordSerializer,
    UserSerializer,
    LoginResponseSerializer,
    UpdatePasswordSerializer,
    LisrUserSerializer,
    )
from .profile_exceptions import UserNotFound, UserNotVerified

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError


def get_login_response(user, request):
    refresh = RefreshToken.for_user(user)
    data = {
        "user": UserSerializer(instance=user, context={'request': request}).data,
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }
    return data

class RegistrationAPIView(generics.GenericAPIView):
    """
        APIViews for signUp
    """
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        user_data = serializers.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        # abs_url = f'{HOST_OF_SERVER}/api/users/verify-email/' + '?token=' + str(token)
        # email_body = f'Hello' \
        #              f'Use this link to activate your email\n ' \
        #              f'The link will be active for 10 minutes \n {abs_url}'
        # data = {'email_body': email_body, 'to_email': user.email,
        #     'email_subject': 'Verify your email'}
        # Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relative_link = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            token = RefreshToken.for_user(user).access_token
            abs_url = 'http://' + current_site + relative_link
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                         abs_url + '?token=' + str(token)
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your password'}
            Util.send_email(data)
        return Response(user, {'success': 'We have  sent you a link to reset your password'}, status=status.HTTP_200_OK)


# class VerifyEmail(views.APIView):
#     """
#         Verifi Email after signUp
#     """
#     serializer_class = EmailVerificationSerializer

#     token_param_config = openapi.Parameter(
#         'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

#     @swagger_auto_schema(manual_parameters=[token_param_config])
#     def get(self, request):
#         token = request.GET.get('token')

#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
#             user = User.objects.get(id=payload['user_id'])
#             if not user.is_verified:
#                 user.is_verified = True
#                 user.is_active = True
#                 user.save()
#             return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
#         except jwt.ExpiredSignatureError:
#             return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
#         except jwt.exceptions.DecodeError:
#             return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    """
        LogIn with email and password
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = LoginSerializer

    @swagger_auto_schema(responses={'200': LoginResponseSerializer()}, tags=['auth'])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        if not user:
            raise exceptions.AuthenticationFailed()
        log(request, user)
        if request.user.is_verified == False:
            raise UserNotVerified()
        return response.Response(data=get_login_response(user, request))

class UsersView(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
               mixins.ListModelMixin,
               viewsets.GenericViewSet):
    """
        Just userView
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = LisrUserSerializer

    def get_queryset(self):
        return User.objects.all()

class ProfileAPIView(generics.GenericAPIView):
    """
        request.user Profile View 
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={'200': UserSerializer()}, tags=['auth'])
    def get(self, request):
        serializer = self.get_serializer(instance=request.user)
        return response.Response(data=serializer.data)

    def patch(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(data=get_login_response(request.user, request.data))
    
    def delete(self, request):
        request.user.delete()
        return response.Response(status.HTTP_200_OK)
        
class PasswordView(generics.GenericAPIView):
    """
        Change password
    """
    serializer_class = UpdatePasswordSerializer

    @swagger_auto_schema(responses={'200': ''}, tags=['auth'])
    def post(self, request):
        serializer = UpdatePasswordSerializer(data=request.data, instance=request.user, context={'request': request})
        serializer.is_valid(True)
        serializer.save()
        return response.Response(status=200)



    @swagger_auto_schema(responses={'200': LoginResponseSerializer()}, tags=['auth'])
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(True)
        password = serializer.validated_data['new_password']
        user = request.user
        if not isinstance(user, User):
            raise UserNotFound()
        user.set_password(password)
        user.save()
        return response.Response(data=get_login_response(user, request))


class DeleteProfilePhoto(APIView):
    """
        Delete users photo
    """
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        request.user.photo.delete()
        return response.Response(status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    """
        LogOUt wiht users refresh token
    """
    serializer_class = LogOutRefreshTokenSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        pass

class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one '})

            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token},
                            status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator():
                return Response({'error': 'Token is not valid, please request a new one '})


class ResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class BasketViewset(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Basket.objects.all().order_by('-id')
    serializer_class = BasketSerializer

    def get_serializer_context(self):
        context = super(BasketViewset, self).get_serializer_context()
        context.update({"request": self.request})
        return context