from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .external_token_service import ExternalTokenService
import logging

logger = logging.getLogger(__name__)


class ExternalTokenAuthentication(BaseAuthentication):
    """
    Harici kimlik yönetim servisi token'ları ile authentication
    """
    
    def authenticate(self, request):
        """
        Harici token ile authentication
        
        Args:
            request: HTTP request
            
        Returns:
            Tuple[User, token]: (user, token) veya None
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        
        try:
            token_service = ExternalTokenService()
            success, user_data, error_message = token_service.validate_external_token(token)
            
            if not success:
                logger.warning(f"Harici token doğrulama başarısız: {error_message}")
                return None
            
            # Kullanıcıyı bul veya oluştur
            from apps.users.models import User
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
            
            # Request'e harici token bilgilerini ekle
            request.external_token = token
            request.external_user_data = user_data
            
            return (user, token)
            
        except Exception as e:
            logger.error(f"Harici token authentication hatası: {str(e)}")
            return None
    
    def authenticate_header(self, request):
        """
        Authentication header'ı döndür
        
        Args:
            request: HTTP request
            
        Returns:
            str: Authentication header
        """
        return 'Bearer'
