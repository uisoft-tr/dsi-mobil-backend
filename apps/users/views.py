from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User
from .serializers import UserSerializer, UserUpdateSerializer, AvatarUploadSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Kullanıcı profil görüntüleme ve güncelleme"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def get_serializer_context(self):
        """Context'e request'i ekle"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    """Kullanıcı profil güncelleme"""
    serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        user_serializer = UserSerializer(request.user, context={'request': request})
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list_view(request):
    """Kullanıcı listesi (admin veya yetkili kullanıcılar için)"""
    if not request.user.is_staff:
        return Response({'error': 'Bu işlem için yetkiniz yok.'}, status=status.HTTP_403_FORBIDDEN)
    
    users = User.objects.all()
    serializer = UserSerializer(users, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_avatar_view(request):
    """Avatar yükleme"""
    serializer = AvatarUploadSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        # Güncellenmiş kullanıcı bilgilerini döndür
        user_serializer = UserSerializer(request.user, context={'request': request})
        return Response({
            'success': True,
            'message': 'Avatar başarıyla yüklendi',
            'user': user_serializer.data
        }, status=status.HTTP_200_OK)
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_avatar_view(request):
    """Avatar silme"""
    if request.user.avatar:
        # Eski avatar dosyasını sil
        request.user.avatar.delete(save=False)
        request.user.avatar = None
        request.user.save()
        
        # Güncellenmiş kullanıcı bilgilerini döndür
        user_serializer = UserSerializer(request.user, context={'request': request})
        return Response({
            'success': True,
            'message': 'Avatar başarıyla silindi',
            'user': user_serializer.data
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'success': False,
            'message': 'Silinecek avatar bulunamadı'
        }, status=status.HTTP_404_NOT_FOUND)
