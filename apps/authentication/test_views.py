from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .external_auth_service import ExternalAuthService


@api_view(['POST'])
@permission_classes([AllowAny])
def test_external_auth_view(request):
    """Harici kimlik yönetim servisi test endpoint'i"""
    try:
        auth_service = ExternalAuthService()
        
        # Test verileri
        test_data = {
            "usernameOrEmail": "emrah.sander@uisoft.tech",
            "password": "i^+cY#fionKWAM"
        }
        
        # Harici servis ile doğrulama
        success, user_data, error_message = auth_service.authenticate_user(
            test_data["usernameOrEmail"], 
            test_data["password"]
        )
        
        return Response({
            'success': success,
            'user_data': user_data,
            'error_message': error_message,
            'test_data': test_data,
            'service_config': {
                'base_url': auth_service.base_url,
                'app_id': auth_service.application_id,
                'timeout': auth_service.timeout
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Test hatası: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
