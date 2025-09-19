import requests
import logging
from django.conf import settings
from typing import Dict, Optional, Tuple, List
from datetime import datetime
import json
from .mock_data import MOCK_ABP_RESPONSE

logger = logging.getLogger(__name__)


class DSITahsilatAPIService:
    """DSİ Tahsilat API entegrasyonu"""
    
    def __init__(self):
        self.base_url = getattr(settings, 'DSI_API_BASE_URL', 'https://altayapi.dsi.gov.tr')
        self.timeout = getattr(settings, 'DSI_API_TIMEOUT', 30)
        self.use_mock = getattr(settings, 'DSI_API_USE_MOCK', False)  # Gerçek API kullan
    
    def tahsilat_listele(self, tckn: str = None, vkn: str = None, 
                        baslangic_tarihi: datetime = None, bitis_tarihi: datetime = None,
                        sadece_odenmemis: bool = False) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        DSİ Tahsilat Listele API'sini çağır
        
        Args:
            tckn: TC Kimlik No
            vkn: Vergi Kimlik No
            baslangic_tarihi: Başlangıç tarihi
            bitis_tarihi: Bitiş tarihi
            sadece_odenmemis: Sadece ödenmemiş kayıtlar mı
            
        Returns:
            Tuple[bool, Optional[Dict], Optional[str]]: (success, data, error_message)
        """
        try:
            # Mock data kullan
            if self.use_mock:
                logger.info("Mock data kullanılıyor")
                data = MOCK_ABP_RESPONSE.copy()
                
                # Sadece ödenmemiş kayıtlar filtresi uygula
                if sadece_odenmemis:
                    data['result']['tahsilatListe'] = [
                        item for item in data['result']['tahsilatListe'] 
                        if item['kalanAnaparaBorc'] > 0
                    ]
                
                # Tarih filtresi uygula (basit)
                if baslangic_tarihi or bitis_tarihi:
                    filtered_list = []
                    for item in data['result']['tahsilatListe']:
                        item_date = datetime.fromisoformat(item['tahakkukDonemi'].replace('Z', '+00:00'))
                        if baslangic_tarihi and item_date < baslangic_tarihi:
                            continue
                        if bitis_tarihi and item_date > bitis_tarihi:
                            continue
                        filtered_list.append(item)
                    data['result']['tahsilatListe'] = filtered_list
                
                # Özet bilgilerini yeniden hesapla
                tahsilat_liste = data['result']['tahsilatListe']
                data['result']['anaParaBorc'] = sum(item['anaParaBorc'] for item in tahsilat_liste)
                data['result']['yapilanToplamTahsilat'] = sum(item['yapilanToplamTahsilat'] for item in tahsilat_liste)
                data['result']['toplamKalanAnaparaBorc'] = sum(item['kalanAnaparaBorc'] for item in tahsilat_liste)
                
                return True, data['result'], None
            
            # Gerçek API çağrısı
            url = f"{self.base_url}/api/services/app/Tahsilat/TahsilatListeleEDevlet"
            
            # Parametreleri hazırla
            params = {}
            if tckn:
                params['TCKN'] = tckn
            if vkn:
                params['VKN'] = vkn
            if baslangic_tarihi:
                params['BaslangicTarihi'] = baslangic_tarihi.strftime('%Y-%m-%dT%H:%M:%S')
            if bitis_tarihi:
                params['BitisTarihi'] = bitis_tarihi.strftime('%Y-%m-%dT%H:%M:%S')
            if sadece_odenmemis is not None:
                params['SadeceOdenmemisKayitlarMi'] = str(sadece_odenmemis).lower()
            
            headers = {
                'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
                'Authorization': 'null',
                'Connection': 'keep-alive',
                'Content-Length': '0',
                'Origin': 'https://altayapi.dsi.gov.tr',
                'Referer': 'https://altayapi.dsi.gov.tr/swagger/index.html',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
                'accept': 'text/plain',
                'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"'
            }
            
            logger.info(f"DSİ API çağrısı: {url} - Params: {params}")
            
            # Session kullan ve cookie ekle
            session = requests.Session()
            session.cookies.set('BIGipServeraltayapi_https_pool', '2751991980.47873.0000')
            
            # SSL doğrulamasını atla
            session.verify = False
            
            # POST metodu kullan
            response = session.post(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            
            logger.info(f"DSİ API Response Status: {response.status_code}")
            logger.info(f"DSİ API Response: {response.text[:500]}...")
            
            if response.status_code == 200:
                data = response.json()
                
                # ABP response formatını kontrol et
                if data.get('success', False):
                    result = data.get('result', {})
                    return True, result, None
                else:
                    error_msg = data.get('error', {}).get('message', 'Bilinmeyen hata')
                    return False, None, f"DSİ API Hatası: {error_msg}"
            else:
                return False, None, f"DSİ API HTTP Hatası: {response.status_code} - {response.text[:200]}"
                
        except requests.exceptions.Timeout:
            logger.error("DSİ API zaman aşımı")
            return False, None, "DSİ API zaman aşımı"
        except requests.exceptions.ConnectionError:
            logger.error("DSİ API bağlantı hatası")
            return False, None, "DSİ API bağlantı hatası"
        except Exception as e:
            logger.error(f"DSİ API beklenmeyen hata: {str(e)}")
            return False, None, f"Beklenmeyen hata: {str(e)}"
    
    def tahsilat_detay_getir(self, tahsilat_id: int) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Belirli bir tahsilat kaydının detayını getir
        
        Args:
            tahsilat_id: Tahsilat ID
            
        Returns:
            Tuple[bool, Optional[Dict], Optional[str]]: (success, data, error_message)
        """
        try:
            url = f"{self.base_url}/api/services/app/Tahsilat/TahsilatDetayGetir"
            
            params = {
                'TahsilatId': tahsilat_id
            }
            
            headers = {
                'accept': 'application/json',
                'content-type': 'application/json',
                'user-agent': 'DSI-Mobil-Backend/1.0'
            }
            
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success', False):
                    return True, data.get('result'), None
                else:
                    error_msg = data.get('error', {}).get('message', 'Bilinmeyen hata')
                    return False, None, f"DSİ API Hatası: {error_msg}"
            else:
                return False, None, f"DSİ API HTTP Hatası: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Tahsilat detay getirme hatası: {str(e)}")
            return False, None, f"Beklenmeyen hata: {str(e)}"
    
    def tahsilat_odeme_yap(self, tahsilat_id: int, odeme_tutari: float, 
                          odeme_tarihi: datetime = None) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Tahsilat ödemesi yap (eğer API varsa)
        
        Args:
            tahsilat_id: Tahsilat ID
            odeme_tutari: Ödeme tutarı
            odeme_tarihi: Ödeme tarihi
            
        Returns:
            Tuple[bool, Optional[Dict], Optional[str]]: (success, data, error_message)
        """
        try:
            url = f"{self.base_url}/api/services/app/Tahsilat/TahsilatOdemeYap"
            
            payload = {
                'TahsilatId': tahsilat_id,
                'OdemeTutari': odeme_tutari,
                'OdemeTarihi': (odeme_tarihi or datetime.now()).strftime('%Y-%m-%dT%H:%M:%S')
            }
            
            headers = {
                'accept': 'application/json',
                'content-type': 'application/json',
                'user-agent': 'DSI-Mobil-Backend/1.0'
            }
            
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success', False):
                    return True, data.get('result'), None
                else:
                    error_msg = data.get('error', {}).get('message', 'Bilinmeyen hata')
                    return False, None, f"DSİ API Hatası: {error_msg}"
            else:
                return False, None, f"DSİ API HTTP Hatası: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Tahsilat ödeme hatası: {str(e)}")
            return False, None, f"Beklenmeyen hata: {str(e)}"
    
    def tahsilat_detay_getir(self, tahsilat_id: int) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Tahsilat detay bilgilerini getir
        
        Args:
            tahsilat_id: Tahsilat ID
            
        Returns:
            Tuple[bool, Optional[Dict], Optional[str]]: (success, data, error_message)
        """
        try:
            # Mock data kullan
            if self.use_mock:
                logger.info("Mock data kullanılıyor - Tahsilat Detay")
                # Mock detay verisi
                mock_detail = {
                    "tahsilatId": tahsilat_id,
                    "tahakkukNo": f"202111808000000{tahsilat_id}",
                    "gelirTuru": "08 - İçme Kullanma ve Endüstri Suyu Tesislerine İlişkin Yatırım Bedeli Geri Ödeme Gelirleri",
                    "borcunKonusu": f"Test tahsilat detayı - ID: {tahsilat_id}",
                    "cariId": 1792,
                    "anaParaBorc": 100000.00,
                    "yapilanToplamTahsilat": 50000.00,
                    "kalanAnaparaBorc": 50000.00,
                    "tahakkukDonemi": "2024-01-31T00:00:00",
                    "taksitler": [
                        {
                            "taksitNo": 1,
                            "taksitTutari": 25000.00,
                            "vadeTarihi": "2024-02-28T00:00:00",
                            "odemeDurumu": "Ödendi",
                            "odemeTarihi": "2024-02-15T00:00:00"
                        },
                        {
                            "taksitNo": 2,
                            "taksitTutari": 25000.00,
                            "vadeTarihi": "2024-03-31T00:00:00",
                            "odemeDurumu": "Beklemede",
                            "odemeTarihi": None
                        }
                    ],
                    "odemeGecmisi": [
                        {
                            "odemeTarihi": "2024-02-15T00:00:00",
                            "odemeTutari": 25000.00,
                            "odemeYontemi": "Banka Havalesi",
                            "referansNo": "REF001"
                        }
                    ]
                }
                return True, mock_detail, None
            
            # Gerçek API çağrısı
            url = f"{self.base_url}/api/services/app/Tahsilat/VTahsilatDetayGetirEDevlet"
            
            # Parametreleri hazırla
            params = {
                'tahsilatId': tahsilat_id
            }
            
            headers = {
                'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
                'Authorization': 'null',
                'Connection': 'keep-alive',
                'Content-Length': '0',
                'Origin': 'https://altayapi.dsi.gov.tr',
                'Referer': 'https://altayapi.dsi.gov.tr/swagger/index.html',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
                'accept': 'text/plain',
                'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"'
            }
            
            logger.info(f"DSİ Tahsilat Detay API çağrısı: {url} - Params: {params}")
            
            # Session kullan ve cookie ekle
            session = requests.Session()
            session.cookies.set('BIGipServeraltayapi_https_pool', '2751991980.47873.0000')
            
            # SSL doğrulamasını atla
            session.verify = False
            
            # POST metodu kullan
            response = session.post(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            
            logger.info(f"DSİ Tahsilat Detay API Response Status: {response.status_code}")
            logger.info(f"DSİ Tahsilat Detay API Response: {response.text[:500]}...")
            
            if response.status_code == 200:
                data = response.json()
                
                # ABP response formatını kontrol et
                if data.get('success', False):
                    result = data.get('result', {})
                    return True, result, None
                else:
                    error_msg = data.get('error', {}).get('message', 'Bilinmeyen hata')
                    return False, None, f"DSİ API Hatası: {error_msg}"
            else:
                return False, None, f"DSİ API HTTP Hatası: {response.status_code} - {response.text[:200]}"
                
        except requests.exceptions.Timeout:
            logger.error("DSİ Tahsilat Detay API zaman aşımı")
            return False, None, "DSİ API zaman aşımı"
        except requests.exceptions.ConnectionError:
            logger.error("DSİ Tahsilat Detay API bağlantı hatası")
            return False, None, "DSİ API bağlantı hatası"
        except Exception as e:
            logger.exception(f"Beklenmeyen DSİ Tahsilat Detay API hatası: {e}")
            return False, None, f"Beklenmeyen hata: {str(e)}"
    
    def tahsilat_belge_getir(self, tahsilat_id: int) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Tahsilat detay belgesini PDF olarak getir (base64 formatında)
        
        Args:
            tahsilat_id: Tahsilat ID
            
        Returns:
            Tuple[bool, Optional[Dict], Optional[str]]: (success, data, error_message)
        """
        try:
            # Mock data kullan
            if self.use_mock:
                logger.info("Mock data kullanılıyor - Tahsilat Belge")
                # Mock PDF belge verisi (base64)
                mock_pdf_base64 = "JVBERi0xLjQKJcOkw7zDtsO8CjIgMCBvYmoKPDwKL0xlbmd0aCAzIDAgUgovVHlwZSAvUGFnZQovUmVzb3VyY2VzIDw8Ci9Gb250IDw8Ci9GMSAKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvSGVsdmV0aWNhCj4+Cj4+Cj4+Ci9QYXJlbnQgMSAwIFIKPj4KZW5kb2JqCjMgMCBvYmoKNDQKZW5kb2JqCjEgMCBvYmoKPDwKL1R5cGUgL1BhZ2VzCi9LaWRzIFsyIDAgUl0KL0NvdW50IDEKL01lZGlhQm94IFswIDAgNTk1IDg0Ml0KPj4KZW5kb2JqCjQgMCBvYmoKPDwKL1R5cGUgL0NhdGFsb2cKL1BhZ2VzIDEgMCBSCj4+CmVuZG9iagp4cmVmCjAgNQowMDAwMDAwMDAwIDY1NTM1IGYKMDAwMDAwMDAwOSAwMDAwMCBuCjAwMDAwMDAwNTggMDAwMDAgbgowMDAwMDAwMTE1IDAwMDAwIG4KMDAwMDAwMDI2MiAwMDAwMCBuCnRyYWlsZXIKPDwKL1NpemUgNQovUm9vdCA0IDAgUgo+PgpzdGFydHhyZWYKMzIxCiUlRU9G"
                
                mock_belge = {
                    "tahsilatId": tahsilat_id,
                    "belgeAdi": f"Tahsilat_Detay_{tahsilat_id}.pdf",
                    "belge": mock_pdf_base64,
                    "belgeBoyutu": len(mock_pdf_base64),
                    "olusturmaTarihi": "2025-01-19T12:00:00Z",
                    "sonucBilgisi": {
                        "sonucKodu": "001",
                        "sonucAciklamasi": "Belge başarıyla oluşturuldu."
                    }
                }
                return True, mock_belge, None
            
            # Gerçek API çağrısı
            url = f"{self.base_url}/api/services/app/Tahsilat/TahsilatBelgeGetirEDevlet"
            
            # Parametreleri hazırla
            params = {
                'tahsilatId': tahsilat_id
            }
            
            headers = {
                'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
                'Authorization': 'null',
                'Connection': 'keep-alive',
                'Content-Length': '0',
                'Origin': 'https://altayapi.dsi.gov.tr',
                'Referer': 'https://altayapi.dsi.gov.tr/swagger/index.html',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
                'accept': 'text/plain',
                'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"'
            }
            
            logger.info(f"DSİ Tahsilat Belge API çağrısı: {url} - Params: {params}")
            
            # Session kullan ve cookie ekle
            session = requests.Session()
            session.cookies.set('BIGipServeraltayapi_https_pool', '2751991980.47873.0000')
            
            # SSL doğrulamasını atla
            session.verify = False
            
            # POST metodu kullan
            response = session.post(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            
            logger.info(f"DSİ Tahsilat Belge API Response Status: {response.status_code}")
            logger.info(f"DSİ Tahsilat Belge API Response: {response.text[:500]}...")
            
            if response.status_code == 200:
                data = response.json()
                
                # ABP response formatını kontrol et
                if data.get('success', False):
                    result = data.get('result', {})
                    return True, result, None
                else:
                    error_msg = data.get('error', {}).get('message', 'Bilinmeyen hata')
                    return False, None, f"DSİ API Hatası: {error_msg}"
            else:
                return False, None, f"DSİ API HTTP Hatası: {response.status_code} - {response.text[:200]}"
                
        except requests.exceptions.Timeout:
            logger.error("DSİ Tahsilat Belge API zaman aşımı")
            return False, None, "DSİ API zaman aşımı"
        except requests.exceptions.ConnectionError:
            logger.error("DSİ Tahsilat Belge API bağlantı hatası")
            return False, None, "DSİ API bağlantı hatası"
        except Exception as e:
            logger.exception(f"Beklenmeyen DSİ Tahsilat Belge API hatası: {e}")
            return False, None, f"Beklenmeyen hata: {str(e)}"
