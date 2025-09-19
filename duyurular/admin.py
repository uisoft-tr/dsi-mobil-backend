from django.contrib import admin
from .models import Duyuru


@admin.register(Duyuru)
class DuyuruAdmin(admin.ModelAdmin):
    """Duyuru admin paneli"""
    
    list_display = [
        'baslik', 
        'kategori', 
        'tip', 
        'tarih', 
        'yayinlandi', 
        'aktif',
        'sira'
    ]
    list_filter = ['kategori', 'tip', 'yayinlandi', 'aktif', 'tarih']
    search_fields = ['baslik', 'kategori', 'ozet']
    list_editable = ['yayinlandi', 'aktif', 'sira']
    ordering = ['-sira', '-tarih']
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('baslik', 'kategori', 'tip', 'tarih')
        }),
        ('İçerik', {
            'fields': ('ozet', 'detaylar', 'resim')
        }),
        ('Durum', {
            'fields': ('aktif', 'yayinlandi', 'sira')
        }),
    )
    
    def get_queryset(self, request):
        """Admin queryset"""
        return super().get_queryset(request).select_related()