from django.contrib import admin
from .models import TahsilatKaydi, TahsilatSorgu, TahsilatOzeti


@admin.register(TahsilatKaydi)
class TahsilatKaydiAdmin(admin.ModelAdmin):
    list_display = [
        'tahakkuk_no', 'gelir_turu', 'ana_para_borc', 'kalan_anapara_borc',
        'odeme_durumu', 'kullanici', 'tahakkuk_donemi', 'aktif'
    ]
    list_filter = ['aktif', 'tahakkuk_donemi', 'kullanici']
    search_fields = ['tahakkuk_no', 'gelir_turu', 'borcun_konusu']
    readonly_fields = ['tahsilat_id', 'harici_id', 'sorgu_tarihi', 'son_guncelleme']
    ordering = ['-tahakkuk_donemi']
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('tahsilat_id', 'tahakkuk_no', 'gelir_turu', 'borcun_konusu')
        }),
        ('Mali Bilgiler', {
            'fields': ('ana_para_borc', 'yapilan_toplam_tahsilat', 'kalan_anapara_borc')
        }),
        ('Sistem Bilgileri', {
            'fields': ('cari_id', 'tahakkuk_donemi', 'harici_id', 'kullanici', 'aktif')
        }),
        ('Zaman Bilgileri', {
            'fields': ('sorgu_tarihi', 'son_guncelleme'),
            'classes': ('collapse',)
        })
    )


@admin.register(TahsilatSorgu)
class TahsilatSorguAdmin(admin.ModelAdmin):
    list_display = [
        'kullanici', 'sorgu_tipi', 'sorgu_degeri', 'sorgu_tarihi',
        'basarili', 'donen_kayit_sayisi'
    ]
    list_filter = ['basarili', 'sorgu_tipi', 'sorgu_tarihi', 'kullanici']
    search_fields = ['sorgu_degeri', 'hata_mesaji']
    readonly_fields = ['sorgu_tarihi']
    ordering = ['-sorgu_tarihi']
    
    fieldsets = (
        ('Sorgu Bilgileri', {
            'fields': ('kullanici', 'sorgu_tipi', 'sorgu_degeri')
        }),
        ('Tarih Aralığı', {
            'fields': ('baslangic_tarihi', 'bitis_tarihi', 'sadece_odenmemis')
        }),
        ('Sonuç', {
            'fields': ('basarili', 'donen_kayit_sayisi', 'hata_mesaji', 'sorgu_tarihi')
        })
    )


@admin.register(TahsilatOzeti)
class TahsilatOzetiAdmin(admin.ModelAdmin):
    list_display = [
        'tahsilat_sorgu', 'ana_para_borc', 'toplam_kalan_anapara_borc',
        'sonuc_kodu'
    ]
    list_filter = ['sonuc_kodu']
    readonly_fields = ['tahsilat_sorgu']
    
    fieldsets = (
        ('Sorgu Bilgisi', {
            'fields': ('tahsilat_sorgu',)
        }),
        ('Mali Özet', {
            'fields': ('ana_para_borc', 'yapilan_toplam_tahsilat', 'toplam_kalan_anapara_borc')
        }),
        ('Sonuç', {
            'fields': ('sonuc_kodu', 'sonuc_aciklamasi')
        })
    )
