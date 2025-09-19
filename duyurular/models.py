from django.db import models
from django.utils import timezone


class DuyuruTipi(models.TextChoices):
    """Duyuru tipleri"""
    NORMAL = 'normal', 'Normal'
    ONEMLI = 'onemli', 'Önemli'
    ACIL = 'acil', 'Acil'
    BILGI = 'bilgi', 'Bilgi'


class Duyuru(models.Model):
    """Duyuru modeli"""
    
    # Temel bilgiler
    baslik = models.CharField(max_length=200, verbose_name="Başlık")
    kategori = models.CharField(max_length=100, verbose_name="Kategori")
    tip = models.CharField(
        max_length=20, 
        choices=DuyuruTipi.choices, 
        default=DuyuruTipi.NORMAL,
        verbose_name="Tip"
    )
    
    # İçerik
    ozet = models.TextField(max_length=500, verbose_name="Özet")
    detaylar = models.TextField(verbose_name="Detaylar")
    
    # Görsel
    resim = models.ImageField(
        upload_to='duyurular/resimler/', 
        null=True, 
        blank=True,
        verbose_name="Resim"
    )
    
    # Tarih bilgileri
    tarih = models.DateTimeField(default=timezone.now, verbose_name="Tarih")
    olusturma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturma Tarihi")
    guncelleme_tarihi = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    # Durum
    aktif = models.BooleanField(default=True, verbose_name="Aktif")
    yayinlandi = models.BooleanField(default=False, verbose_name="Yayınlandı")
    
    # Sıralama
    sira = models.PositiveIntegerField(default=0, verbose_name="Sıra")
    
    class Meta:
        verbose_name = "Duyuru"
        verbose_name_plural = "Duyurular"
        ordering = ['-sira', '-tarih']
    
    def __str__(self):
        return f"{self.baslik} ({self.kategori})"
    
    @property
    def tip_renk(self):
        """Tip'e göre renk döndürür"""
        renkler = {
            DuyuruTipi.NORMAL: '#28a745',  # Yeşil
            DuyuruTipi.ONEMLI: '#dc3545',  # Kırmızı
            DuyuruTipi.ACIL: '#ffc107',    # Sarı
            DuyuruTipi.BILGI: '#17a2b8',   # Mavi
        }
        return renkler.get(self.tip, '#28a745')
    
    @property
    def tip_etiket(self):
        """Tip'e göre etiket metni döndürür"""
        etiketler = {
            DuyuruTipi.NORMAL: 'NORMAL',
            DuyuruTipi.ONEMLI: 'ÖNEMLİ',
            DuyuruTipi.ACIL: 'ACİL',
            DuyuruTipi.BILGI: 'BİLGİ',
        }
        return etiketler.get(self.tip, 'NORMAL')