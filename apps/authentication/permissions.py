from rest_framework.permissions import BasePermission
from .external_token_service import ExternalTokenService
import logging

logger = logging.getLogger(__name__)


class ExternalTokenPermission(BasePermission):
    """
    Harici kimlik yönetim servisi token'ı ile yetkilendirme
    """
    
    def has_permission(self, request, view):
        """
        Harici token ile yetki kontrolü
        
        Args:
            request: HTTP request
            view: API view
            
        Returns:
            bool: Yetki var mı
        """
        # Authorization header'ından token'ı al
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return False
        
        token = auth_header.split(' ')[1]
        
        try:
            token_service = ExternalTokenService()
            success, user_data, error_message = token_service.validate_external_token(token)
            
            if success and user_data:
                # Request'e harici token bilgilerini ekle
                request.external_token = token
                request.external_user_data = user_data
                return True
            else:
                logger.warning(f"Harici token doğrulama başarısız: {error_message}")
                return False
                
        except Exception as e:
            logger.error(f"Harici token yetki kontrolü hatası: {str(e)}")
            return False


class ExternalTokenOrJWTPermission(BasePermission):
    """
    Harici token veya Django JWT token ile yetkilendirme
    """
    
    def has_permission(self, request, view):
        """
        Harici token veya Django JWT ile yetki kontrolü
        
        Args:
            request: HTTP request
            view: API view
            
        Returns:
            bool: Yetki var mı
        """
        # Önce harici token'ı dene
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return False
        
        token = auth_header.split(' ')[1]
        
        try:
            # Harici token'ı dene
            token_service = ExternalTokenService()
            success, user_data, error_message = token_service.validate_external_token(token)
            
            if success and user_data:
                request.external_token = token
                request.external_user_data = user_data
                return True
        except Exception as e:
            logger.warning(f"Harici token kontrolü hatası: {str(e)}")
        
        # Harici token başarısızsa Django JWT'yi dene
        try:
            from rest_framework_simplejwt.authentication import JWTAuthentication
            jwt_auth = JWTAuthentication()
            user, token = jwt_auth.authenticate(request)
            if user:
                request.user = user
                return True
        except Exception as e:
            logger.warning(f"Django JWT kontrolü hatası: {str(e)}")
        
        return False
