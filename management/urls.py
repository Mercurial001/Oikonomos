from django.urls import path
from . import views
from django.conf.urls.static import static
from economics import settings

urlpatterns = [
    path('', views.index, name='homepage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
