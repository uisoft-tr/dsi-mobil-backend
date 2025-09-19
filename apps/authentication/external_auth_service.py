import requests
import logging
from django.conf import settings
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class ExternalAuthService:
    """Harici kimlik yönetim servisi entegrasyonu"""
    
    def __init__(self):
        self.base_url = getattr(settings, 'EXTERNAL_AUTH_BASE_URL', 'https://yenikysdevapi.dsi.gov.tr')
        self.application_id = getattr(settings, 'EXTERNAL_AUTH_APP_ID', '1021')
        self.timeout = getattr(settings, 'EXTERNAL_AUTH_TIMEOUT', 30)
    
    def authenticate_user(self, username_or_email: str, password: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Harici kimlik yönetim servisi ile kullanıcı doğrulama
        
        Args:
            username_or_email: Kullanıcı adı veya email
            password: Şifre
            
        Returns:
            Tuple[bool, Optional[Dict], Optional[str]]: (success, user_data, error_message)
        """
        try:
            url = f"{self.base_url}/api/Auth/Login/Application/{self.application_id}"
            
            payload = {
                "usernameOrEmail": username_or_email,
                "password": password
            }
            
            headers = {
                'accept': 'text/plain',
                'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
                'content-type': 'application/json',
                'origin': self.base_url,
                'referer': f'{self.base_url}/swagger/index.html',
                'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
            }
            
            # Session oluştur ve cookie'leri yönet
            session = requests.Session()
            
            response = session.post(
                url, 
                json=payload, 
                headers=headers, 
                timeout=self.timeout
            )
            

            # Response detaylarını logla
            logger.info(f"Response Status: {response.status_code}")
            logger.info(f"Response Headers: {dict(response.headers)}")
            logger.info(f"Response Text: {response.text[:500]}...")
            
            if response.status_code == 200:
                # Başarılı giriş
                try:
                    user_data = response.json()
                except:
                    user_data = {"message": response.text}
                logger.info(f"Kullanıcı başarıyla doğrulandı: {username_or_email}")
                return True, user_data, None
            elif response.status_code == 401:
                # Geçersiz kimlik bilgileri
                logger.warning(f"Geçersiz kimlik bilgileri: {username_or_email}")
                return False, None, "Geçersiz kullanıcı adı veya şifre"
            elif response.status_code == 403:
                # Hesap devre dışı veya yetkisiz
                logger.warning(f"Hesap devre dışı veya yetkisiz: {username_or_email}")
                return False, None, "Hesap devre dışı veya yetkisiz"
            else:
                # Diğer hatalar
                logger.error(f"Kimlik doğrulama hatası: {response.status_code} - {response.text}")
                return False, None, f"Kimlik doğrulama servisi hatası: {response.status_code} - {response.text[:200]}"
                
        except requests.exceptions.Timeout:
            logger.error(f"Kimlik doğrulama servisi zaman aşımı: {username_or_email}")
            return False, None, "Kimlik doğrulama servisi zaman aşımı"
        except requests.exceptions.ConnectionError:
            logger.error(f"Kimlik doğrulama servisi bağlantı hatası: {username_or_email}")
            return False, None, "Kimlik doğrulama servisi bağlantı hatası"
        except Exception as e:
            logger.error(f"Beklenmeyen hata: {str(e)}")
            return False, None, "Beklenmeyen bir hata oluştu"
    
    def get_user_info(self, token: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Token ile kullanıcı bilgilerini getir
        
        Args:
            token: Kimlik doğrulama token'ı
            
        Returns:
            Tuple[bool, Optional[Dict], Optional[str]]: (success, user_data, error_message)
        """
        try:
            url = f"{self.base_url}/api/Auth/UserInfo"
            
            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {token}'
            }
            
            response = requests.get(
                url, 
                headers=headers, 
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                user_data = response.json()
                return True, user_data, None
            else:
                logger.error(f"Kullanıcı bilgisi alma hatası: {response.status_code} - {response.text}")
                return False, None, f"Kullanıcı bilgisi alma hatası: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Kullanıcı bilgisi alma hatası: {str(e)}")
            return False, None, "Kullanıcı bilgisi alma hatası"
    
    def refresh_token(self, refresh_token: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Refresh token ile yeni access token al
        
        Args:
            refresh_token: Refresh token
            
        Returns:
            Tuple[bool, Optional[Dict], Optional[str]]: (success, token_data, error_message)
        """
        try:
            url = f"{self.base_url}/api/Auth/Refresh"
            
            payload = {
                "refreshToken": refresh_token
            }
            
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                url, 
                json=payload, 
                headers=headers, 
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                token_data = response.json()
                return True, token_data, None
            else:
                logger.error(f"Token yenileme hatası: {response.status_code} - {response.text}")
                return False, None, f"Token yenileme hatası: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Token yenileme hatası: {str(e)}")
            return False, None, "Token yenileme hatası"
