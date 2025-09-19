from django.urls import path
from . import views
from . import test_views

urlpatterns = [
    # Harici kimlik yönetim servisi endpoints
    path('external-login/', views.external_login_view, name='external_login'),
    path('test-external-auth/', test_views.test_external_auth_view, name='test_external_auth'),
    
    # Yerel Django authentication endpoints (opsiyonel)
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('profile/', views.user_profile_view, name='user_profile'),
]
