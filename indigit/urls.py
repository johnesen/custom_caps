from django.urls import path
from .views import *


urlpatterns = [
    path('', IndigitView.as_view()),
]
