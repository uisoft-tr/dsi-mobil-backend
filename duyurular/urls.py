from django.urls import path
from . import views

urlpatterns = [
    # Public endpoints
    path('liste/', views.DuyuruListeView.as_view(), name='duyuru_liste'),
    path('detay/<int:id>/', views.DuyuruDetayView.as_view(), name='duyuru_detay'),
    path('kategoriler/', views.duyuru_kategorileri_view, name='duyuru_kategorileri'),
    path('tipler/', views.duyuru_tipleri_view, name='duyuru_tipleri'),
    path('istatistikler/', views.duyuru_istatistikleri_view, name='duyuru_istatistikleri'),
    
    # Admin endpoints
    path('olustur/', views.DuyuruOlusturView.as_view(), name='duyuru_olustur'),
    path('guncelle/<int:id>/', views.DuyuruGuncelleView.as_view(), name='duyuru_guncelle'),
    path('sil/<int:id>/', views.DuyuruSilView.as_view(), name='duyuru_sil'),
    path('yayinla/<int:duyuru_id>/', views.duyuru_yayinla_view, name='duyuru_yayinla'),
]
