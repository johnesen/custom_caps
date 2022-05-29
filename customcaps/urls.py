from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_url


urlpatterns = [
    path('nurjon/', admin.site.urls),
    path('api/caps/', include('caps.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/baner/', include('baner.urls')),
    path('api/digits/', include('indigit.urls')),
    path('api/users/', include('users.urls')),
]

urlpatterns += doc_url

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
