from rest_framework import serializers
from .models import TahsilatKaydi, TahsilatSorgu, TahsilatOzeti
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()


class TahsilatKaydiSerializer(serializers.ModelSerializer):
    """Tahsilat kaydı serializer"""
    odeme_durumu = serializers.ReadOnlyField()
    
    class Meta:
        model = TahsilatKaydi
        fields = [
            'id', 'tahsilat_id', 'tahakkuk_no', 'gelir_turu', 'borcun_konusu',
            'cari_id', 'ana_para_borc', 'yapilan_toplam_tahsilat', 'kalan_anapara_borc',
            'tahakkuk_donemi', 'harici_id', 'odeme_durumu', 'sorgu_tarihi', 'son_guncelleme'
        ]
        read_only_fields = ['id', 'kullanici', 'sorgu_tarihi', 'son_guncelleme']


class TahsilatSorguSerializer(serializers.ModelSerializer):
    """Tahsilat sorgu serializer"""
    
    class Meta:
        model = TahsilatSorgu
        fields = [
            'id', 'sorgu_tipi', 'sorgu_degeri', 'baslangic_tarihi', 'bitis_tarihi',
            'sadece_odenmemis', 'sorgu_tarihi', 'basarili', 'hata_mesaji', 'donen_kayit_sayisi'
        ]
        read_only_fields = ['id', 'kullanici', 'sorgu_tarihi', 'basarili', 'hata_mesaji', 'donen_kayit_sayisi']


class TahsilatOzetiSerializer(serializers.ModelSerializer):
    """Tahsilat özeti serializer"""
    
    class Meta:
        model = TahsilatOzeti
        fields = [
            'ana_para_borc', 'yapilan_toplam_tahsilat', 'toplam_kalan_anapara_borc',
            'sonuc_kodu', 'sonuc_aciklamasi'
        ]


class TahsilatSorguRequestSerializer(serializers.Serializer):
    """Tahsilat sorgu isteği serializer"""
    tckn = serializers.CharField(max_length=11, required=False, help_text="TC Kimlik No")
    vkn = serializers.CharField(max_length=10, required=False, help_text="Vergi Kimlik No")
    baslangic_tarihi = serializers.DateTimeField(required=False, help_text="Başlangıç tarihi")
    bitis_tarihi = serializers.DateTimeField(required=False, help_text="Bitiş tarihi")
    sadece_odenmemis = serializers.BooleanField(default=False, help_text="Sadece ödenmemiş kayıtlar")
    
    def validate(self, attrs):
        """Sorgu parametrelerini doğrula"""
        tckn = attrs.get('tckn')
        vkn = attrs.get('vkn')
        
        # En az bir kimlik numarası gerekli
        if not tckn and not vkn:
            raise serializers.ValidationError("TCKN veya VKN'den en az biri gerekli")
        
        # İkisi birden verilmemeli
        if tckn and vkn:
            raise serializers.ValidationError("TCKN ve VKN'den sadece biri verilebilir")
        
        # TCKN format kontrolü
        if tckn and (not tckn.isdigit() or len(tckn) != 11):
            raise serializers.ValidationError("TCKN 11 haneli sayı olmalıdır")
        
        # VKN format kontrolü
        if vkn and (not vkn.isdigit() or len(vkn) != 10):
            raise serializers.ValidationError("VKN 10 haneli sayı olmalıdır")
        
        # Tarih kontrolü
        baslangic = attrs.get('baslangic_tarihi')
        bitis = attrs.get('bitis_tarihi')
        
        if baslangic and bitis and baslangic > bitis:
            raise serializers.ValidationError("Başlangıç tarihi bitiş tarihinden büyük olamaz")
        
        return attrs


class DSITahsilatResponseSerializer(serializers.Serializer):
    """DSİ API'den dönen tahsilat listesi serializer"""
    tahsilat_id = serializers.IntegerField()
    tahakkuk_no = serializers.CharField()
    gelir_turu = serializers.CharField()
    borcun_konusu = serializers.CharField()
    cari_id = serializers.IntegerField()
    ana_para_borc = serializers.DecimalField(max_digits=15, decimal_places=2)
    yapilan_toplam_tahsilat = serializers.DecimalField(max_digits=15, decimal_places=2)
    kalan_anapara_borc = serializers.DecimalField(max_digits=15, decimal_places=2)
    tahakkuk_donemi = serializers.DateTimeField()
    harici_id = serializers.IntegerField(source='id')


class DSITahsilatOzetSerializer(serializers.Serializer):
    """DSİ API'den dönen tahsilat özeti serializer"""
    ana_para_borc = serializers.DecimalField(max_digits=15, decimal_places=2)
    yapilan_toplam_tahsilat = serializers.DecimalField(max_digits=15, decimal_places=2)
    toplam_kalan_anapara_borc = serializers.DecimalField(max_digits=15, decimal_places=2)
    sonuc_bilgisi = serializers.DictField()


class TahsilatListeResponseSerializer(serializers.Serializer):
    """Tahsilat listesi response serializer"""
    tahsilat_liste = DSITahsilatResponseSerializer(many=True)
    ana_para_borc = serializers.DecimalField(max_digits=15, decimal_places=2)
    yapilan_toplam_tahsilat = serializers.DecimalField(max_digits=15, decimal_places=2)
    toplam_kalan_anapara_borc = serializers.DecimalField(max_digits=15, decimal_places=2)
    sonuc_bilgisi = serializers.DictField()
    harici_id = serializers.IntegerField()


class TahsilatDetaySerializer(serializers.ModelSerializer):
    """Tahsilat detay serializer (kayıtlı veriler)"""
    odeme_durumu = serializers.ReadOnlyField()
    kullanici_adi = serializers.CharField(source='kullanici.full_name', read_only=True)
    
    class Meta:
        model = TahsilatKaydi
        fields = [
            'id', 'tahsilat_id', 'tahakkuk_no', 'gelir_turu', 'borcun_konusu',
            'cari_id', 'ana_para_borc', 'yapilan_toplam_tahsilat', 'kalan_anapara_borc',
            'tahakkuk_donemi', 'harici_id', 'odeme_durumu', 'kullanici_adi',
            'sorgu_tarihi', 'son_guncelleme', 'aktif'
        ]
