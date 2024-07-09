from django.urls import path
from . import views
from django.conf.urls.static import static
from economics import settings

urlpatterns = [
    path('', views.index, name='homepage'),
    path('login/', views.authentication, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('registration/', views.registration, name='registration'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('terms-of-use/', views.terms_of_use, name='terms-of-use'),
    path('about/', views.about_us, name='about'),
    path('contact-us/', views.contact_us_page, name='contact-us')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
