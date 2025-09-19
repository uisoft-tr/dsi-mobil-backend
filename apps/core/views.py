from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.authentication.permissions import ExternalTokenPermission, ExternalTokenOrJWTPermission


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check_view(request):
    """Sistem sağlık kontrolü"""
    return Response({
        'status': 'OK',
        'message': 'DSI Mobil Backend API çalışıyor',
        'version': '1.0.0'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_info_view(request):
    """API bilgileri"""
    return Response({
        'name': 'DSI Mobil Backend API',
        'version': '1.0.0',
        'description': 'React Native projesi için Django REST API',
        'endpoints': {
            'authentication': '/api/v1/auth/',
            'users': '/api/v1/users/',
            'core': '/api/v1/core/',
            'documentation': '/swagger/',
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([ExternalTokenPermission])
def external_token_info_view(request):
    """Harici token bilgileri (sadece harici token ile erişilebilir)"""
    external_data = getattr(request, 'external_user_data', {})
    external_token = getattr(request, 'external_token', None)
    
    return Response({
        'message': 'Harici token ile erişim başarılı',
        'external_token': external_token[:20] + '...' if external_token else None,
        'user_data': external_data,
        'timestamp': request.META.get('HTTP_DATE', 'N/A')
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([ExternalTokenOrJWTPermission])
def flexible_auth_view(request):
    """Esnek authentication (harici token veya Django JWT)"""
    external_data = getattr(request, 'external_user_data', None)
    user = getattr(request, 'user', None)
    
    response_data = {
        'message': 'Authentication başarılı',
        'auth_type': 'external_token' if external_data else 'django_jwt',
        'timestamp': request.META.get('HTTP_DATE', 'N/A')
    }
    
    if external_data:
        response_data['external_user_data'] = external_data
        response_data['external_token'] = getattr(request, 'external_token', None)[:20] + '...'
    else:
        response_data['django_user'] = {
            'id': user.id if user else None,
            'email': user.email if user else None,
            'username': user.username if user else None
        }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def django_jwt_only_view(request):
    """Sadece Django JWT ile erişilebilir"""
    return Response({
        'message': 'Django JWT ile erişim başarılı',
        'user': {
            'id': request.user.id,
            'email': request.user.email,
            'username': request.user.username
        }
    }, status=status.HTTP_200_OK)