from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class ExternalTokenMiddleware(MiddlewareMixin):
    """
    Harici kimlik yönetim servisinden gelen token'ları işleyen middleware
    """
    
    def process_request(self, request):
        # Authorization header'ından token'ı al
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return
        
        token = auth_header.split(' ')[1]
        
        try:
            # Django JWT token'ını doğrula
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            
            # Kullanıcıyı al
            try:
                user = User.objects.get(id=user_id)
                request.user = user
                request.external_token = token  # Harici token'ı request'e ekle
            except User.DoesNotExist:
                logger.warning(f"Token'da belirtilen kullanıcı bulunamadı: {user_id}")
                
        except (InvalidToken, TokenError) as e:
            logger.warning(f"Geçersiz token: {str(e)}")
            return
