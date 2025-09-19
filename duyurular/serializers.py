from rest_framework import serializers
from django.utils import timezone
from .models import Duyuru, DuyuruTipi


class DuyuruSerializer(serializers.ModelSerializer):
    """Duyuru serializer"""
    
    tip_renk = serializers.ReadOnlyField()
    tip_etiket = serializers.ReadOnlyField()
    resim_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Duyuru
        fields = [
            'id',
            'baslik',
            'kategori',
            'tip',
            'tip_renk',
            'tip_etiket',
            'ozet',
            'detaylar',
            'resim',
            'resim_url',
            'tarih',
            'olusturma_tarihi',
            'guncelleme_tarihi',
            'aktif',
            'yayinlandi',
            'sira'
        ]
        read_only_fields = ['olusturma_tarihi', 'guncelleme_tarihi']
    
    def get_resim_url(self, obj):
        """Resim URL'ini döndürür"""
        if obj.resim:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.resim.url)
            return obj.resim.url
        return None


class DuyuruListeSerializer(serializers.ModelSerializer):
    """Duyuru liste serializer (kısa bilgiler)"""
    
    tip_renk = serializers.ReadOnlyField()
    tip_etiket = serializers.ReadOnlyField()
    resim_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Duyuru
        fields = [
            'id',
            'baslik',
            'kategori',
            'tip',
            'tip_renk',
            'tip_etiket',
            'ozet',
            'resim_url',
            'tarih',
            'yayinlandi',
            'sira'
        ]
    
    def get_resim_url(self, obj):
        """Resim URL'ini döndürür"""
        if obj.resim:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.resim.url)
            return obj.resim.url
        return None


class DuyuruOlusturSerializer(serializers.ModelSerializer):
    """Duyuru oluşturma serializer"""
    
    class Meta:
        model = Duyuru
        fields = [
            'baslik',
            'kategori',
            'tip',
            'ozet',
            'detaylar',
            'resim',
            'tarih',
            'aktif',
            'yayinlandi',
            'sira'
        ]
    
    def validate_tarih(self, value):
        """Tarih validasyonu"""
        if value and value > timezone.now():
            raise serializers.ValidationError("Gelecek tarih olamaz.")
        return value


class DuyuruGuncelleSerializer(serializers.ModelSerializer):
    """Duyuru güncelleme serializer"""
    
    class Meta:
        model = Duyuru
        fields = [
            'baslik',
            'kategori',
            'tip',
            'ozet',
            'detaylar',
            'resim',
            'tarih',
            'aktif',
            'yayinlandi',
            'sira'
        ]
    
    def validate_tarih(self, value):
        """Tarih validasyonu"""
        if value and value > timezone.now():
            raise serializers.ValidationError("Gelecek tarih olamaz.")
        return value
