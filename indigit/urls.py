from django.urls import path
from .views import *


urlpatterns = [
    path('indigit/', IndigitView.as_view()),
]
