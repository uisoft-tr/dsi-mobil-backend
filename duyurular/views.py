from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .models import Duyuru, DuyuruTipi
from .serializers import (
    DuyuruSerializer, 
    DuyuruListeSerializer, 
    DuyuruOlusturSerializer,
    DuyuruGuncelleSerializer
)


class DuyuruListeView(generics.ListAPIView):
    """Duyuru listesi (public)"""
    
    serializer_class = DuyuruListeSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        """Aktif ve yayınlanmış duyuruları getir"""
        queryset = Duyuru.objects.filter(aktif=True, yayinlandi=True)
        
        # Kategori filtresi
        kategori = self.request.query_params.get('kategori', None)
        if kategori:
            queryset = queryset.filter(kategori__icontains=kategori)
        
        # Tip filtresi
        tip = self.request.query_params.get('tip', None)
        if tip:
            queryset = queryset.filter(tip=tip)
        
        # Arama
        arama = self.request.query_params.get('arama', None)
        if arama:
            queryset = queryset.filter(
                Q(baslik__icontains=arama) | 
                Q(ozet__icontains=arama) |
                Q(kategori__icontains=arama)
            )
        
        return queryset


class DuyuruDetayView(generics.RetrieveAPIView):
    """Duyuru detayı (public)"""
    
    serializer_class = DuyuruSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    
    def get_queryset(self):
        """Aktif ve yayınlanmış duyuruları getir"""
        return Duyuru.objects.filter(aktif=True, yayinlandi=True)


class DuyuruOlusturView(generics.CreateAPIView):
    """Duyuru oluşturma (admin)"""
    
    serializer_class = DuyuruOlusturSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """Duyuru oluşturma"""
        serializer.save()


class DuyuruGuncelleView(generics.UpdateAPIView):
    """Duyuru güncelleme (admin)"""
    
    serializer_class = DuyuruGuncelleSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        """Tüm duyuruları getir"""
        return Duyuru.objects.all()


class DuyuruSilView(generics.DestroyAPIView):
    """Duyuru silme (admin)"""
    
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        """Tüm duyuruları getir"""
        return Duyuru.objects.all()


@api_view(['GET'])
@permission_classes([AllowAny])
def duyuru_kategorileri_view(request):
    """Duyuru kategorilerini getir"""
    kategoriler = Duyuru.objects.filter(
        aktif=True, 
        yayinlandi=True
    ).values_list('kategori', flat=True).distinct()
    
    return Response({
        'success': True,
        'kategoriler': list(kategoriler)
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def duyuru_tipleri_view(request):
    """Duyuru tiplerini getir"""

    # Tip renklerini manuel olarak tanımla
    tip_renkleri = {
        DuyuruTipi.NORMAL: '#28a745',  # Yeşil
        DuyuruTipi.ONEMLI: '#dc3545',  # Kırmızı
        DuyuruTipi.ACIL: '#ffc107',    # Sarı
        DuyuruTipi.BILGI: '#17a2b8',   # Mavi
    }
    
    tipler = [
        {
            'value': choice[0],
            'label': choice[1],
            'renk': tip_renkleri.get(choice[0], '#28a745')
        }
        for choice in DuyuruTipi.choices
    ]
    
    return Response({
        'success': True,
        'tipler': tipler
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def duyuru_istatistikleri_view(request):
    """Duyuru istatistikleri"""
    toplam_duyuru = Duyuru.objects.filter(aktif=True).count()
    yayinlanan_duyuru = Duyuru.objects.filter(aktif=True, yayinlandi=True).count()
    bekleyen_duyuru = Duyuru.objects.filter(aktif=True, yayinlandi=False).count()
    
    # Kategori bazında sayılar
    kategori_sayilari = {}
    for kategori in Duyuru.objects.filter(aktif=True, yayinlandi=True).values_list('kategori', flat=True).distinct():
        kategori_sayilari[kategori] = Duyuru.objects.filter(
            aktif=True, 
            yayinlandi=True, 
            kategori=kategori
        ).count()
    
    # Tip bazında sayılar
    tip_sayilari = {}
    for tip_value, tip_label in DuyuruTipi.choices:
        tip_sayilari[tip_value] = Duyuru.objects.filter(
            aktif=True, 
            yayinlandi=True, 
            tip=tip_value
        ).count()
    
    return Response({
        'success': True,
        'istatistikler': {
            'toplam_duyuru': toplam_duyuru,
            'yayinlanan_duyuru': yayinlanan_duyuru,
            'bekleyen_duyuru': bekleyen_duyuru,
            'kategori_sayilari': kategori_sayilari,
            'tip_sayilari': tip_sayilari
        }
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def duyuru_yayinla_view(request, duyuru_id):
    """Duyuru yayınla/yayından kaldır"""
    try:
        duyuru = get_object_or_404(Duyuru, id=duyuru_id)
        
        # Yayın durumunu tersine çevir
        duyuru.yayinlandi = not duyuru.yayinlandi
        duyuru.save()
        
        return Response({
            'success': True,
            'message': f'Duyuru {"yayınlandı" if duyuru.yayinlandi else "yayından kaldırıldı"}',
            'yayinlandi': duyuru.yayinlandi
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Beklenmeyen hata: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)