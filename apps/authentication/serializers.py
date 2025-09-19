from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from apps.users.models import User


class ExternalLoginSerializer(serializers.Serializer):
    """Harici kimlik yönetim servisi ile giriş"""
    usernameOrEmail = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username_or_email = attrs.get('usernameOrEmail')
        password = attrs.get('password')

        if not username_or_email or not password:
            raise serializers.ValidationError('Kullanıcı adı/email ve şifre gerekli.')
        
        attrs['username_or_email'] = username_or_email
        return attrs


class LoginSerializer(serializers.Serializer):
    """Yerel Django kullanıcı girişi (opsiyonel)"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('Geçersiz email veya şifre.')
            if not user.is_active:
                raise serializers.ValidationError('Hesap devre dışı.')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Email ve şifre gerekli.')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'password', 'password_confirm')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Şifreler eşleşmiyor.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Yeni şifreler eşleşmiyor.")
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Mevcut şifre yanlış.")
        return value
