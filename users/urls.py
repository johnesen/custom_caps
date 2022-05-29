from django.urls import path, include
from users import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('basket', views.BasketViewset, 'basket')
router.register('', views.UsersView, 'users')

urlpatterns = [
    path('signup/', views.RegistrationAPIView.as_view()),
    path('signin/', views.LoginAPIView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('verify-email/', views.VerifyEmail.as_view()),
    path('profile/password/', views.PasswordView.as_view()),
    path('profile/', views.ProfileAPIView.as_view()),
    path('', include(router.urls)),
    path('profile/delete_photo/', views.DeleteProfilePhoto.as_view(), name='delete_photo'),
    path('password-recovery/', views.RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('password-recovery/<uidb64>/<token>/', views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-recovery-complete/', views.ResetPasswordAPIView.as_view()),
]
