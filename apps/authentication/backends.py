from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from .external_token_service import ExternalTokenService
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class ExternalTokenBackend(BaseBackend):
    """
    Harici kimlik yönetim servisi token'ları ile authentication
    """
    
    def authenticate(self, request, external_token=None, **kwargs):
        """
        Harici token ile kullanıcı doğrulama
        
        Args:
            request: HTTP request
            external_token: Harici kimlik yönetim servisi token'ı
            
        Returns:
            User: Doğrulanmış kullanıcı veya None
        """
        if not external_token:
            return None
        
        try:
            token_service = ExternalTokenService()
            success, user_data, error_message = token_service.validate_external_token(external_token)
            
            if not success:
                logger.warning(f"Harici token doğrulama başarısız: {error_message}")
                return None
            
            # Kullanıcıyı bul veya oluştur
            email = user_data.get('email')
            if not email:
                logger.warning("Harici token'da email bulunamadı")
                return None
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Kullanıcı yoksa oluştur
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=user_data.get('name', ''),
                    last_name=user_data.get('surname', ''),
                    is_active=True,
                    is_verified=True
                )
            
            # Kullanıcı bilgilerini güncelle
            user.first_name = user_data.get('name', user.first_name)
            user.last_name = user_data.get('surname', user.last_name)
            user.is_active = True
            user.is_verified = True
            user.save()
            
            # Request'e harici token'ı ekle
            request.external_token = external_token
            request.external_user_data = user_data
            
            return user
            
        except Exception as e:
            logger.error(f"Harici token authentication hatası: {str(e)}")
            return None
    
    def get_user(self, user_id):
        """
        Kullanıcı ID'si ile kullanıcıyı getir
        
        Args:
            user_id: Kullanıcı ID'si
            
        Returns:
            User: Kullanıcı veya None
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
