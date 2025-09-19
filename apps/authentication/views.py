from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from .serializers import LoginSerializer, RegisterSerializer, ChangePasswordSerializer, ExternalLoginSerializer
from .external_auth_service import ExternalAuthService
from apps.users.models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def external_login_view(request):
    """Harici kimlik yönetim servisi ile giriş"""
    serializer = ExternalLoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    username_or_email = serializer.validated_data['username_or_email']
    password = serializer.validated_data['password']
    
    # Harici kimlik yönetim servisi ile doğrulama
    auth_service = ExternalAuthService()
    success, user_data, error_message = auth_service.authenticate_user(username_or_email, password)
    
    if not success:
        return Response({
            'error': error_message or 'Kimlik doğrulama başarısız'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Kullanıcıyı yerel veritabanında bul veya oluştur
    try:
        # Email ile kullanıcıyı bul
        user = User.objects.get(email=username_or_email)
    except User.DoesNotExist:
        try:
            # Username ile kullanıcıyı bul
            user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            # Kullanıcı yoksa oluştur
            first_name = ''
            last_name = ''
            if user_data and 'tokenPayload' in user_data:
                token_payload = user_data['tokenPayload']
                first_name = token_payload.get('name', '')
                last_name = token_payload.get('surname', '')
            
            user = User.objects.create_user(
                username=username_or_email,
                email=username_or_email if '@' in username_or_email else f"{username_or_email}@dsi.gov.tr",
                first_name=first_name,
                last_name=last_name,
                is_active=True,
                is_verified=True
            )
    
    # Kullanıcıyı güncelle
    if user_data and 'tokenPayload' in user_data:
        token_payload = user_data['tokenPayload']
        user.first_name = token_payload.get('name', user.first_name)
        user.last_name = token_payload.get('surname', user.last_name)
        user.is_active = True
        user.is_verified = True
        user.save()
    
    # JWT token oluştur
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'is_active': user.is_active,
            'is_verified': user.is_verified,
        },
        'external_data': user_data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Yerel Django kullanıcı girişi (opsiyonel)"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': user.phone,
                'is_active': user.is_active,
            }
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Kullanıcı kaydı"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': user.phone,
                'is_active': user.is_active,
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """Şifre değiştirme"""
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Şifre başarıyla değiştirildi.'}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Kullanıcı çıkışı"""
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Başarıyla çıkış yapıldı.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Geçersiz token.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    """Kullanıcı profil bilgileri"""
    user = request.user
    return Response({
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone': user.phone,
        'is_active': user.is_active,
        'date_joined': user.date_joined,
        'last_login': user.last_login,
    })
