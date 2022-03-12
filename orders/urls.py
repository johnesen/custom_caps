from django.urls import path
from .views import *

urlpatterns = [
    path('orders/', OrderListView.as_view()),
    path('orders/<int:pk>/', OrderDetView.as_view()),
    path('orders/create/', OrderCreateView.as_view()),
    path('orders/item/create/', OrderItemCreateView.as_view()),
]
