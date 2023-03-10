from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from usuarios.views import logar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('usuarios.urls')),
    path('divulgar/', include('divulgar.urls')),
    path('adotar/', include('adotar.urls')),
    path('', logar, name='login'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
