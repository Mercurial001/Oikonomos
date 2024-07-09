from django.urls import path
from . import views
from django.conf.urls.static import static
from economics import settings

urlpatterns = [
    path('<str:username>', views.index, name='personal-homepage'),
    path('remove-expense/<int:id>/<str:username>/', views.remove_personal_expenses, name='remove-expense'),
    path('remove-fund/<int:id>/<str:username>/', views.remove_fund, name='remove-fund'),
    path('create-net-worth-flow/<str:username>/', views.create_net_worth_flow, name='create-new-worth-flow'),
    path('filter-receiver-funds/', views.filter_personal_fund, name='filter-personal-fund'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
