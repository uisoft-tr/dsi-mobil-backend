from django.urls import path
from . import views

urlpatterns = [
    # Tahsilat sorgu ve listeleme
    path('sorgu/', views.TahsilatSorguView.as_view(), name='tahsilat_sorgu'),
    path('liste/', views.TahsilatListeView.as_view(), name='tahsilat_liste'),
    path('detay/<int:pk>/', views.TahsilatDetayView.as_view(), name='tahsilat_detay'),
    path('detay-getir/<int:tahsilat_id>/', views.tahsilat_detay_getir_view, name='tahsilat_detay_getir'),
    path('belge-getir/<int:tahsilat_id>/', views.tahsilat_belge_getir_view, name='tahsilat_belge_getir'),
    path('sorgu-gecmisi/', views.TahsilatSorguGecmisiView.as_view(), name='tahsilat_sorgu_gecmisi'),
    
    # İstatistikler ve işlemler
    path('istatistikler/', views.tahsilat_istatistikleri_view, name='tahsilat_istatistikleri'),
    path('yenile/<int:tahsilat_id>/', views.tahsilat_yenile_view, name='tahsilat_yenile'),
    
]
