import requests
import logging
from django.conf import settings
from typing import Dict, Optional, Tuple
import jwt
from datetime import datetime

logger = logging.getLogger(__name__)


class ExternalTokenService:
    """Harici kimlik yönetim servisi token yönetimi"""
    
    def __init__(self):
        self.base_url = getattr(settings, 'EXTERNAL_AUTH_BASE_URL', 'https://yenikysdevapi.dsi.gov.tr')
        self.timeout = getattr(settings, 'EXTERNAL_AUTH_TIMEOUT', 30)
    
    def validate_external_token(self, token: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Harici kimlik yönetim servisi token'ını doğrula
        
        Args:
            token: Harici kimlik yönetim servisi token'ı
            
        Returns:
            Tuple[bool, Optional[Dict], Optional[str]]: (success, user_data, error_message)
        """
        try:
            # Token'ı decode et (JWT olmayabilir, sadece string olabilir)
            # Önce harici servise token doğrulama isteği gönder
            url = f"{self.base_url}/api/Auth/ValidateToken"
            
            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {token}',
                'content-type': 'application/json'
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
                logger.warning(f"Token doğrulama hatası: {response.status_code}")
                return False, None, f"Token doğrulama hatası: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Token doğrulama hatası: {str(e)}")
            return False, None, f"Token doğrulama hatası: {str(e)}"
    
    def get_user_info_from_token(self, token: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Token'dan kullanıcı bilgilerini al
        
        Args:
            token: Harici kimlik yönetim servisi token'ı
            
        Returns:
            Tuple[bool, Optional[Dict], Optional[str]]: (success, user_data, error_message)
        """
        try:
            url = f"{self.base_url}/api/Auth/UserInfo"
            
            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {token}',
                'content-type': 'application/json'
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
                logger.warning(f"Kullanıcı bilgisi alma hatası: {response.status_code}")
                return False, None, f"Kullanıcı bilgisi alma hatası: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Kullanıcı bilgisi alma hatası: {str(e)}")
            return False, None, f"Kullanıcı bilgisi alma hatası: {str(e)}"
    
    def is_token_valid(self, token: str) -> bool:
        """
        Token'ın geçerli olup olmadığını kontrol et
        
        Args:
            token: Harici kimlik yönetim servisi token'ı
            
        Returns:
            bool: Token geçerli mi
        """
        success, _, _ = self.validate_external_token(token)
        return success
