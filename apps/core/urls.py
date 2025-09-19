from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check_view, name='health_check'),
    path('info/', views.api_info_view, name='api_info'),
    path('external-token-info/', views.external_token_info_view, name='external_token_info'),
    path('flexible-auth/', views.flexible_auth_view, name='flexible_auth'),
    path('django-jwt-only/', views.django_jwt_only_view, name='django_jwt_only'),
]
