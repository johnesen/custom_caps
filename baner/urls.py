from django.urls import path
from .views import *


urlpatterns = [
    path('', BanerListView.as_view()),
]
