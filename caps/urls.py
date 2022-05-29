from django.urls import path
from .views import *


urlpatterns = [
    path('', CapsListView.as_view()),
    path('<int:pk>/', CapDetailAPIView.as_view()),
    # path('?ordering=price', CapsListView.as_view(), name="order by ++"),
    # path('?ordering=-price', CapsListView.as_view(), name="order by --"),
    # path('?ordering=-created_data', CapsListView.as_view(), name="order by new or old"),
    path('brand/', BrandListView.as_view()),
    path('brand/<slug:slug_url>/', BrandCapListAPIView.as_view()),
    path('favorite/', FavouriteListView.as_view()),
    path('favorite/<int:pk>/', FavouriteDeailView.as_view()),
    path('basket/', BasketListView.as_view()),
    path('basket/<int:pk>/', BasketDetailView.as_view()),
]
