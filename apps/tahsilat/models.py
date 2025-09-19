from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class TahsilatKaydi(models.Model):
    """Tahsilat kaydı modeli"""
    
    # Harici API'den gelen veriler
    tahsilat_id = models.IntegerField(unique=True, help_text="DSİ API'den gelen tahsilat ID")
    tahakkuk_no = models.CharField(max_length=50, help_text="Tahakkuk numarası")
    gelir_turu = models.CharField(max_length=200, help_text="Gelir türü")
    borcun_konusu = models.TextField(help_text="Borçun konusu")
    cari_id = models.IntegerField(help_text="Cari ID")
    ana_para_borc = models.DecimalField(max_digits=15, decimal_places=2, help_text="Ana para borç")
    yapilan_toplam_tahsilat = models.DecimalField(max_digits=15, decimal_places=2, help_text="Yapılan toplam tahsilat")
    kalan_anapara_borc = models.DecimalField(max_digits=15, decimal_places=2, help_text="Kalan ana para borç")
    tahakkuk_donemi = models.DateTimeField(help_text="Tahakkuk dönemi", null=True, blank=True)
    harici_id = models.IntegerField(help_text="Harici sistem ID")
    
    # Yerel sistem alanları
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tahsilat_kayitlari')
    sorgu_tarihi = models.DateTimeField(default=timezone.now, help_text="Sorgu tarihi")
    son_guncelleme = models.DateTimeField(auto_now=True)
    aktif = models.BooleanField(default=True, help_text="Kayıt aktif mi")
    
    class Meta:
        verbose_name = 'Tahsilat Kaydı'
        verbose_name_plural = 'Tahsilat Kayıtları'
        ordering = ['-tahakkuk_donemi']
        indexes = [
            models.Index(fields=['tahsilat_id']),
            models.Index(fields=['tahakkuk_no']),
            models.Index(fields=['kullanici', 'tahakkuk_donemi']),
        ]
    
    def __str__(self):
        return f"{self.tahakkuk_no} - {self.gelir_turu[:50]}"
    
    @property
    def odeme_durumu(self):
        """Ödeme durumunu hesapla"""
        if self.kalan_anapara_borc <= 0:
            return "Ödendi"
        elif self.yapilan_toplam_tahsilat > 0:
            return "Kısmi Ödendi"
        else:
            return "Ödenmedi"


class TahsilatSorgu(models.Model):
    """Tahsilat sorgu geçmişi"""
    
    SORGU_TIPI_CHOICES = [
        ('TCKN', 'TC Kimlik No'),
        ('VKN', 'Vergi Kimlik No'),
    ]
    
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tahsilat_sorgulari')
    sorgu_tipi = models.CharField(max_length=4, choices=SORGU_TIPI_CHOICES)
    sorgu_degeri = models.CharField(max_length=20, help_text="TCKN veya VKN")
    baslangic_tarihi = models.DateTimeField(null=True, blank=True)
    bitis_tarihi = models.DateTimeField(null=True, blank=True)
    sadece_odenmemis = models.BooleanField(default=False)
    sorgu_tarihi = models.DateTimeField(default=timezone.now)
    basarili = models.BooleanField(default=True)
    hata_mesaji = models.TextField(blank=True, null=True)
    donen_kayit_sayisi = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Tahsilat Sorgusu'
        verbose_name_plural = 'Tahsilat Sorguları'
        ordering = ['-sorgu_tarihi']
    
    def __str__(self):
        return f"{self.sorgu_tipi}: {self.sorgu_degeri} - {self.sorgu_tarihi.strftime('%d.%m.%Y %H:%M')}"


class TahsilatOzeti(models.Model):
    """Tahsilat özeti (toplam bilgiler)"""
    
    tahsilat_sorgu = models.OneToOneField(TahsilatSorgu, on_delete=models.CASCADE, related_name='ozet')
    ana_para_borc = models.DecimalField(max_digits=15, decimal_places=2, help_text="Toplam ana para borç")
    yapilan_toplam_tahsilat = models.DecimalField(max_digits=15, decimal_places=2, help_text="Toplam yapılan tahsilat")
    toplam_kalan_anapara_borc = models.DecimalField(max_digits=15, decimal_places=2, help_text="Toplam kalan ana para borç")
    sonuc_kodu = models.CharField(max_length=10, help_text="Sonuç kodu")
    sonuc_aciklamasi = models.CharField(max_length=200, help_text="Sonuç açıklaması")
    
    class Meta:
        verbose_name = 'Tahsilat Özeti'
        verbose_name_plural = 'Tahsilat Özetleri'
    
    def __str__(self):
        return f"Özet - {self.tahsilat_sorgu.sorgu_degeri}"
