from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'full_name', 'phone', 
                 'avatar', 'avatar_url', 'is_verified', 'is_active', 'date_joined', 'last_login')
        read_only_fields = ('id', 'is_verified', 'is_active', 'date_joined', 'last_login')
    
    def get_avatar_url(self, obj):
        """Avatar URL'ini döndürür"""
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'avatar')

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class AvatarUploadSerializer(serializers.ModelSerializer):
    """Avatar yükleme için özel serializer"""
    class Meta:
        model = User
        fields = ('avatar',)
    
    def validate_avatar(self, value):
        """Avatar validasyonu"""
        if value:
            # Dosya boyutu kontrolü (5MB)
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("Avatar dosyası 5MB'dan büyük olamaz.")
            
            # Dosya formatı kontrolü
            allowed_formats = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if value.content_type not in allowed_formats:
                raise serializers.ValidationError("Sadece JPEG, PNG ve GIF formatları desteklenir.")
        
        return value
