from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('update-profile/', views.update_profile_view, name='update_profile'),
    path('list/', views.user_list_view, name='user_list'),
    path('upload-avatar/', views.upload_avatar_view, name='upload_avatar'),
    path('delete-avatar/', views.delete_avatar_view, name='delete_avatar'),
]
