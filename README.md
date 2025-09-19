
# DSI Mobil Backend

React Native projesi için Django REST API backend uygulaması.

## 🚀 Özellikler

- **Django 4.2** ve **Django REST Framework** ile modern API
- **JWT Authentication** ile güvenli kimlik doğrulama
- **PostgreSQL** veritabanı desteği
- **Redis** ile caching ve Celery task queue
- **Docker** ve **Docker Compose** ile containerization
- **CORS** desteği (React Native için)
- **Swagger/OpenAPI** dokümantasyonu
- **Celery** ile asenkron task işleme

## 📋 Gereksinimler

- Python 3.11+
- Docker ve Docker Compose
- PostgreSQL 15+
- Redis 7+

## 🛠️ Kurulum

### Docker ile (Önerilen)

1. Projeyi klonlayın:
```bash
git clone <repository-url>
cd dsi-mobil-backend
```

2. Environment dosyasını oluşturun:
```bash
cp env.example .env
```

3. Docker Compose ile servisleri başlatın:
```bash
docker-compose up --build
```

4. Veritabanı migrasyonlarını çalıştırın:
```bash
docker-compose exec web python manage.py migrate
```

5. Superuser oluşturun:
```bash
docker-compose exec web python manage.py createsuperuser
```

### Manuel Kurulum

1. Virtual environment oluşturun:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

2. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

3. Environment değişkenlerini ayarlayın:
```bash
cp env.example .env
# .env dosyasını düzenleyin
```

4. Veritabanı migrasyonlarını çalıştırın:
```bash
python manage.py migrate
```

5. Superuser oluşturun:
```bash
python manage.py createsuperuser
```

6. Sunucuyu başlatın:
```bash
python manage.py runserver
```

## 📚 API Dokümantasyonu

API dokümantasyonuna erişim:
- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **JSON Schema**: http://localhost:8000/swagger.json

## 🔗 API Endpoints

### Kimlik Doğrulama (`/api/v1/auth/`)
- `POST /external-login/` - Harici kimlik yönetim servisi ile giriş
- `POST /test-external-auth/` - Harici kimlik servisi test endpoint'i
- `POST /login/` - Yerel Django kullanıcı girişi (opsiyonel)
- `POST /register/` - Kullanıcı kaydı (opsiyonel)
- `POST /logout/` - Kullanıcı çıkışı
- `POST /change-password/` - Şifre değiştirme
- `GET /profile/` - Kullanıcı profil bilgileri

### Harici Kimlik Yönetim Servisi Kullanımı

#### Giriş Yapma
```bash
curl -X POST "http://localhost:8001/api/v1/auth/external-login/" \
  -H "Content-Type: application/json" \
  -d '{
    "usernameOrEmail": "emrah.sander@uisoft.tech",
    "password": "your-password"
  }'
```

**Başarılı Yanıt:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "emrah.sander@uisoft.tech",
    "first_name": "Emrah",
    "last_name": "SANDER",
    "is_active": true,
    "is_verified": true
  },
  "external_data": {
    "accessToken": {...},
    "tokenPayload": {...}
  }
}
```

#### Test Endpoint'i
```bash
curl -X POST "http://localhost:8001/api/v1/auth/test-external-auth/"
```

#### Profil Bilgileri
```bash
curl -X GET "http://localhost:8001/api/v1/auth/profile/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Tahsilat Modülü Kullanımı

#### Tahsilat Sorgusu (VKN ile)
```bash
curl -X POST "http://localhost:8001/api/v1/tahsilat/sorgu/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "vkn": "1620052379",
    "sadece_odenmemis": true
  }'
```

#### Tahsilat Sorgusu (TCKN ile)
```bash
curl -X POST "http://localhost:8001/api/v1/tahsilat/sorgu/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "tckn": "12345678901",
    "baslangic_tarihi": "2024-01-01T00:00:00",
    "bitis_tarihi": "2024-12-31T23:59:59",
    "sadece_odenmemis": false
  }'
```

#### Tahsilat Listesi
```bash
curl -X GET "http://localhost:8001/api/v1/tahsilat/liste/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Tahsilat İstatistikleri
```bash
curl -X GET "http://localhost:8001/api/v1/tahsilat/istatistikler/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Kullanıcılar (`/api/v1/users/`)
- `GET /profile/` - Profil görüntüleme
- `PATCH /update-profile/` - Profil güncelleme
- `POST /upload-avatar/` - Avatar yükleme
- `DELETE /delete-avatar/` - Avatar silme
- `GET /list/` - Kullanıcı listesi (admin)

### Tahsilat (`/api/v1/tahsilat/`)
- `POST /sorgu/` - Tahsilat sorgusu (TCKN/VKN ile)
- `GET /liste/` - Kullanıcının tahsilat kayıtları
- `GET /detay/<id>/` - Tahsilat kaydı detayı
- `GET /detay-getir/<tahsilat_id>/` - Tahsilat detay bilgilerini getir
- `GET /belge-getir/<tahsilat_id>/` - Tahsilat detay belgesini direkt PDF dosyası olarak getir (Public - Auth gerekmez)
- `GET /sorgu-gecmisi/` - Tahsilat sorgu geçmişi
- `GET /istatistikler/` - Tahsilat istatistikleri
- `POST /yenile/<tahsilat_id>/` - Tahsilat kaydını yenile

### Duyurular (`/api/v1/duyurular/`)
- `GET /liste/` - Duyuru listesi (Public - Auth gerekmez)
- `GET /detay/<id>/` - Duyuru detayı (Public - Auth gerekmez)
- `GET /kategoriler/` - Duyuru kategorileri (Public - Auth gerekmez)
- `GET /tipler/` - Duyuru tipleri (Public - Auth gerekmez)
- `GET /istatistikler/` - Duyuru istatistikleri (Public - Auth gerekmez)
- `POST /olustur/` - Duyuru oluşturma (Admin)
- `PUT /guncelle/<id>/` - Duyuru güncelleme (Admin)
- `DELETE /sil/<id>/` - Duyuru silme (Admin)
- `POST /yayinla/<duyuru_id>/` - Duyuru yayınla/yayından kaldır (Admin)

### Sistem (`/api/v1/core/`)
- `GET /health/` - Sistem sağlık kontrolü
- `GET /info/` - API bilgileri

## 🐳 Docker Servisleri

- **web**: Django uygulaması (Port: 8000)
- **db**: PostgreSQL veritabanı (Port: 5432)
- **redis**: Redis cache (Port: 6379)
- **celery**: Celery worker
- **celery-beat**: Celery scheduler

## 🔧 Geliştirme

### Yeni Migration Oluşturma
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### Django Shell
```bash
docker-compose exec web python manage.py shell
```

### Logları İzleme
```bash
docker-compose logs -f web
```

### Test Çalıştırma
```bash
docker-compose exec web python manage.py test
```

## 📁 Proje Yapısı

```
dsi-mobil-backend/
├── apps/
│   ├── authentication/     # Kimlik doğrulama
│   ├── users/             # Kullanıcı yönetimi
│   ├── core/              # Temel uygulama
│   └── tahsilat/          # Tahsilat modülü
├── duyurular/             # Duyurular modülü
├── dsi_mobil_backend/     # Ana proje ayarları
├── static/                # Statik dosyalar
├── media/                 # Medya dosyaları
├── logs/                  # Log dosyaları
├── docker-compose.yml     # Docker Compose yapılandırması
├── Dockerfile            # Docker image tanımı
├── requirements.txt      # Python bağımlılıkları
├── FRONTEND_INTEGRATION.md # Frontend entegrasyon rehberi
└── README.md            # Bu dosya
```

## 🔐 Güvenlik

- JWT token tabanlı kimlik doğrulama
- CORS yapılandırması
- Güvenli şifre validasyonu
- Environment değişkenleri ile hassas bilgi yönetimi

## 🚀 Production

Production ortamı için:

1. `DEBUG=False` ayarlayın
2. Güvenli `SECRET_KEY` oluşturun
3. `ALLOWED_HOSTS` listesini güncelleyin
4. SSL sertifikası kullanın
5. Veritabanı yedekleme stratejisi oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add some amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📚 Dokümantasyon

- [API Dokümantasyonu](http://localhost:8001/swagger/) - Swagger UI
- [API Schema](http://localhost:8001/schema/) - OpenAPI Schema
- [Frontend Entegrasyon Rehberi](./FRONTEND_INTEGRATION.md) - React Native entegrasyonu için detaylı dokümantasyon

## 📞 İletişim

Proje ile ilgili sorularınız için: [emrah.sander@uisoft.tech](mailto:emrah.sander@uisoft.tech)
