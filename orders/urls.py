from django.urls import path, include
from .views import OrderViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('orders', OrderViewset, 'order')

urlpatterns = [
    path('', include(router.urls)),
]
