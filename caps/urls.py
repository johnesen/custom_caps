from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('caps', CapsViewset, 'caps')

urlpatterns = [
    path('', include(router.urls)),
    path('brand/', BrandListView.as_view()),
    path('brand/<slug:slug_url>/', BrandCapListAPIView.as_view()),
]
