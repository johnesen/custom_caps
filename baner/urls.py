from django.urls import path
from .views import *


urlpatterns = [
    path('baners/', BanerListView.as_view()),
]
