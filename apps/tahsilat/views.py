from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction, models
from django.shortcuts import get_object_or_404
from .models import TahsilatKaydi, TahsilatSorgu, TahsilatOzeti
from .serializers import (
    TahsilatKaydiSerializer, TahsilatSorguSerializer, TahsilatOzetiSerializer,
    TahsilatSorguRequestSerializer, TahsilatDetaySerializer
)
from .dsi_api_service import DSITahsilatAPIService
import logging

logger = logging.getLogger(__name__)


class TahsilatSorguView(generics.CreateAPIView):
    """Tahsilat sorgu view"""
    serializer_class = TahsilatSorguRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        """Tahsilat sorgusu yap"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # Sorgu kaydını oluştur
        sorgu = TahsilatSorgu.objects.create(
            kullanici=request.user,
            sorgu_tipi='TCKN' if validated_data.get('tckn') else 'VKN',
            sorgu_degeri=validated_data.get('tckn') or validated_data.get('vkn'),
            baslangic_tarihi=validated_data.get('baslangic_tarihi'),
            bitis_tarihi=validated_data.get('bitis_tarihi'),
            sadece_odenmemis=validated_data.get('sadece_odenmemis', False)
        )
        
        try:
            # DSİ API'yi çağır
            dsi_service = DSITahsilatAPIService()
            success, data, error_message = dsi_service.tahsilat_listele(
                tckn=validated_data.get('tckn'),
                vkn=validated_data.get('vkn'),
                baslangic_tarihi=validated_data.get('baslangic_tarihi'),
                bitis_tarihi=validated_data.get('bitis_tarihi'),
                sadece_odenmemis=validated_data.get('sadece_odenmemis', False)
            )
            
            if success and data:
                # Başarılı sorgu
                sorgu.basarili = True
                sorgu.donen_kayit_sayisi = len(data.get('tahsilatListe', []))
                sorgu.save()
                
                # Tahsilat kayıtlarını kaydet
                tahsilat_kayitlari = self._kayitlari_kaydet(data.get('tahsilatListe', []), request.user, sorgu)
                
                # Özet bilgilerini kaydet
                ozet = self._ozet_kaydet(data, sorgu)
                
                return Response({
                    'sorgu_id': sorgu.id,
                    'basarili': True,
                    'tahsilat_kayitlari': TahsilatKaydiSerializer(tahsilat_kayitlari, many=True).data,
                    'ozet': TahsilatOzetiSerializer(ozet).data if ozet else None,
                    'mesaj': f"{sorgu.donen_kayit_sayisi} adet tahsilat kaydı bulundu"
                }, status=status.HTTP_200_OK)
            else:
                # Hatalı sorgu
                sorgu.basarili = False
                sorgu.hata_mesaji = error_message or "Bilinmeyen hata"
                sorgu.save()
                
                return Response({
                    'sorgu_id': sorgu.id,
                    'basarili': False,
                    'hata': error_message or "Bilinmeyen hata"
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"Tahsilat sorgu hatası: {str(e)}")
            sorgu.basarili = False
            sorgu.hata_mesaji = str(e)
            sorgu.save()
            
            return Response({
                'sorgu_id': sorgu.id,
                'basarili': False,
                'hata': f"Beklenmeyen hata: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _kayitlari_kaydet(self, tahsilat_listesi, kullanici, sorgu):
        """Tahsilat kayıtlarını veritabanına kaydet"""
        kayitlar = []
        
        for item in tahsilat_listesi:
            # Mevcut kaydı kontrol et
            tahsilat_kaydi, created = TahsilatKaydi.objects.get_or_create(
                tahsilat_id=item['tahsilatId'],
                defaults={
                    'tahakkuk_no': item['tahakkukNo'],
                    'gelir_turu': item['gelirTuru'],
                    'borcun_konusu': item['borcunKonusu'],
                    'cari_id': item['cariId'],
                    'ana_para_borc': item['anaParaBorc'],
                    'yapilan_toplam_tahsilat': item['yapilanToplamTahsilat'],
                    'kalan_anapara_borc': item['kalanAnaparaBorc'],
                    'tahakkuk_donemi': item['tahakkukDonemi'],
                    'harici_id': item['id'],
                    'kullanici': kullanici
                }
            )
            
            # Kayıt güncellenmişse güncelle
            if not created:
                tahsilat_kaydi.tahakkuk_no = item['tahakkukNo']
                tahsilat_kaydi.gelir_turu = item['gelirTuru']
                tahsilat_kaydi.borcun_konusu = item['borcunKonusu']
                tahsilat_kaydi.cari_id = item['cariId']
                tahsilat_kaydi.ana_para_borc = item['anaParaBorc']
                tahsilat_kaydi.yapilan_toplam_tahsilat = item['yapilanToplamTahsilat']
                tahsilat_kaydi.kalan_anapara_borc = item['kalanAnaparaBorc']
                tahsilat_kaydi.tahakkuk_donemi = item['tahakkukDonemi']
                tahsilat_kaydi.harici_id = item['id']
                tahsilat_kaydi.aktif = True
                tahsilat_kaydi.save()
            
            kayitlar.append(tahsilat_kaydi)
        
        return kayitlar
    
    def _ozet_kaydet(self, data, sorgu):
        """Özet bilgilerini kaydet"""
        try:
            ozet, created = TahsilatOzeti.objects.get_or_create(
                tahsilat_sorgu=sorgu,
                defaults={
                    'ana_para_borc': data.get('anaParaBorc', 0),
                    'yapilan_toplam_tahsilat': data.get('yapilanToplamTahsilat', 0),
                    'toplam_kalan_anapara_borc': data.get('toplamKalanAnaparaBorc', 0),
                    'sonuc_kodu': data.get('sonucBilgisi', {}).get('sonucKodu', ''),
                    'sonuc_aciklamasi': data.get('sonucBilgisi', {}).get('sonucAciklamasi', '')
                }
            )
            return ozet
        except Exception as e:
            logger.error(f"Özet kaydetme hatası: {str(e)}")
            return None


class TahsilatListeView(generics.ListAPIView):
    """Kullanıcının tahsilat kayıtları listesi"""
    serializer_class = TahsilatDetaySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Kullanıcının tahsilat kayıtlarını getir"""
        return TahsilatKaydi.objects.filter(
            kullanici=self.request.user,
            aktif=True
        ).order_by('-tahakkuk_donemi')


class TahsilatDetayView(generics.RetrieveAPIView):
    """Tahsilat kaydı detayı"""
    serializer_class = TahsilatDetaySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Kullanıcının tahsilat kayıtlarını getir"""
        return TahsilatKaydi.objects.filter(
            kullanici=self.request.user,
            aktif=True
        )


class TahsilatSorguGecmisiView(generics.ListAPIView):
    """Tahsilat sorgu geçmişi"""
    serializer_class = TahsilatSorguSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Kullanıcının sorgu geçmişini getir"""
        return TahsilatSorgu.objects.filter(
            kullanici=self.request.user
        ).order_by('-sorgu_tarihi')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tahsilat_istatistikleri_view(request):
    """Tahsilat istatistikleri"""
    try:
        kullanici = request.user
        
        # Toplam borç
        toplam_borc = TahsilatKaydi.objects.filter(
            kullanici=kullanici,
            aktif=True
        ).aggregate(
            toplam_ana_para=models.Sum('ana_para_borc'),
            toplam_yapilan_tahsilat=models.Sum('yapilan_toplam_tahsilat'),
            toplam_kalan_borc=models.Sum('kalan_anapara_borc')
        )
        
        # Ödeme durumlarına göre sayılar
        odeme_durumlari = {
            'odendi': TahsilatKaydi.objects.filter(
                kullanici=kullanici,
                aktif=True,
                kalan_anapara_borc__lte=0
            ).count(),
            'ksmi_odendi': TahsilatKaydi.objects.filter(
                kullanici=kullanici,
                aktif=True,
                yapilan_toplam_tahsilat__gt=0,
                kalan_anapara_borc__gt=0
            ).count(),
            'odenmedi': TahsilatKaydi.objects.filter(
                kullanici=kullanici,
                aktif=True,
                yapilan_toplam_tahsilat=0
            ).count()
        }
        
        # Toplam sorgu sayısı
        toplam_sorgu = TahsilatSorgu.objects.filter(kullanici=kullanici).count()
        basarili_sorgu = TahsilatSorgu.objects.filter(
            kullanici=kullanici,
            basarili=True
        ).count()
        
        return Response({
            'toplam_borc': toplam_borc,
            'odeme_durumlari': odeme_durumlari,
            'sorgu_istatistikleri': {
                'toplam_sorgu': toplam_sorgu,
                'basarili_sorgu': basarili_sorgu,
                'basarisiz_sorgu': toplam_sorgu - basarili_sorgu
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"İstatistik hesaplama hatası: {str(e)}")
        return Response({
            'hata': f"İstatistik hesaplama hatası: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tahsilat_detay_getir_view(request, tahsilat_id):
    """Tahsilat detay bilgilerini getir (taksitler ve ödeme geçmişi)"""
    try:
        # Önce yerel veritabanından tahsilat kaydını kontrol et
        tahsilat_kaydi = get_object_or_404(TahsilatKaydi, tahsilat_id=tahsilat_id, kullanici=request.user)
        
        # DSİ API'den detay bilgilerini çek
        dsi_service = DSITahsilatAPIService()
        success, data, error_message = dsi_service.tahsilat_detay_getir(tahsilat_id)
        
        if not success:
            return Response({
                'success': False,
                'error': f'DSİ API hatası: {error_message}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Yerel kayıt bilgilerini de ekle
        tahsilat_serializer = TahsilatDetaySerializer(tahsilat_kaydi)
        
        return Response({
            'success': True,
            'tahsilat_kaydi': tahsilat_serializer.data,
            'detay_bilgileri': data,
            'message': 'Tahsilat detay bilgileri başarıyla getirildi'
        }, status=status.HTTP_200_OK)
        
    except TahsilatKaydi.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Tahsilat kaydı bulunamadı'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Tahsilat detay getirme hatası: {str(e)}")
        return Response({
            'success': False,
            'error': f'Beklenmeyen hata: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([])
def tahsilat_belge_getir_view(request, tahsilat_id):
    """Tahsilat detay belgesini PDF olarak getir (public endpoint - authentication gerektirmez)"""
    try:
        import base64
        from django.http import HttpResponse
        
        # DSİ API'den belge bilgilerini çek (kullanıcı kontrolü yok)
        dsi_service = DSITahsilatAPIService()
        success, data, error_message = dsi_service.tahsilat_belge_getir(tahsilat_id)
        
        if not success:
            return Response({
                'success': False,
                'error': f'DSİ API hatası: {error_message}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Base64'ü decode et
        pdf_content = base64.b64decode(data.get('belge', ''))
        
        # PDF response oluştur
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{data.get("belgeAdi", f"tahsilat_{tahsilat_id}.pdf")}"'
        response['Content-Length'] = len(pdf_content)
        
        return response
        
    except Exception as e:
        logger.error(f"Tahsilat belge getirme hatası: {str(e)}")
        return Response({
            'success': False,
            'error': f'Beklenmeyen hata: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tahsilat_yenile_view(request, tahsilat_id):
    """Belirli bir tahsilat kaydını yenile"""
    try:
        tahsilat_kaydi = TahsilatKaydi.objects.get(
            id=tahsilat_id,
            kullanici=request.user,
            aktif=True
        )
        
        # DSİ API'den güncel veriyi al
        dsi_service = DSITahsilatAPIService()
        success, data, error_message = dsi_service.tahsilat_detay_getir(tahsilat_kaydi.tahsilat_id)
        
        if success and data:
            # Kaydı güncelle
            tahsilat_kaydi.ana_para_borc = data.get('anaParaBorc', tahsilat_kaydi.ana_para_borc)
            tahsilat_kaydi.yapilan_toplam_tahsilat = data.get('yapilanToplamTahsilat', tahsilat_kaydi.yapilan_toplam_tahsilat)
            tahsilat_kaydi.kalan_anapara_borc = data.get('kalanAnaparaBorc', tahsilat_kaydi.kalan_anapara_borc)
            tahsilat_kaydi.save()
            
            return Response({
                'basarili': True,
                'mesaj': 'Tahsilat kaydı başarıyla güncellendi',
                'tahsilat': TahsilatDetaySerializer(tahsilat_kaydi).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'basarili': False,
                'hata': error_message or "Güncelleme başarısız"
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except TahsilatKaydi.DoesNotExist:
        return Response({
            'basarili': False,
            'hata': 'Tahsilat kaydı bulunamadı'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Tahsilat yenileme hatası: {str(e)}")
        return Response({
            'basarili': False,
            'hata': f"Beklenmeyen hata: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
