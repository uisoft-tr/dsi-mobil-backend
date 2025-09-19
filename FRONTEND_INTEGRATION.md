# Frontend Entegrasyon Dokümantasyonu

Bu dokümantasyon, React Native frontend uygulamasının Django backend API'si ile entegrasyonu için gerekli bilgileri içerir.

## 📋 İçindekiler

1. [Kimlik Doğrulama (Authentication)](#kimlik-doğrulama-authentication)
2. [Tahsilat Modülü](#tahsilat-modülü)
3. [Duyurular Modülü](#duyurular-modülü)
4. [Hata Yönetimi](#hata-yönetimi)
5. [Örnek Kodlar](#örnek-kodlar)

---

## 🔐 Kimlik Doğrulama (Authentication)

### Base URL
```
https://your-domain.com/api/v1/auth/
```

### 1. Harici Kimlik Yönetim Servisi ile Giriş

#### Endpoint
```
POST /external-login/
```

#### Request Body
```json
{
  "usernameOrEmail": "emrah.sander@uisoft.tech",
  "password": "your-password"
}
```

#### Response (Başarılı)
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

#### Response (Hata)
```json
{
  "error": "Geçersiz kullanıcı adı veya şifre"
}
```

### 2. Token Yenileme

#### Endpoint
```
POST /token/refresh/
```

#### Request Body
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 3. Profil Bilgileri

#### Endpoint
```
GET /profile/
```

#### Headers
```
Authorization: Bearer <access_token>
```

#### Response
```json
{
  "id": 1,
  "email": "emrah.sander@uisoft.tech",
  "first_name": "Emrah",
  "last_name": "SANDER",
  "full_name": "Emrah SANDER",
  "phone": "+905551234567",
  "avatar": "http://localhost:8001/media/avatars/avatar.jpg",
  "avatar_url": "http://localhost:8001/media/avatars/avatar.jpg",
  "is_active": true,
  "is_verified": true,
  "date_joined": "2025-01-19T09:30:00Z",
  "last_login": "2025-01-19T10:30:00Z"
}
```

### 4. Profil Güncelleme

#### Endpoint
```
PATCH /update-profile/
```

#### Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

#### Request Body
```json
{
  "first_name": "Emrah",
  "last_name": "SANDER",
  "phone": "+905551234567"
}
```

#### Response
```json
{
  "id": 1,
  "email": "emrah.sander@uisoft.tech",
  "first_name": "Emrah",
  "last_name": "SANDER",
  "full_name": "Emrah SANDER",
  "phone": "+905551234567",
  "avatar": "http://localhost:8001/media/avatars/avatar.jpg",
  "avatar_url": "http://localhost:8001/media/avatars/avatar.jpg",
  "is_active": true,
  "is_verified": true,
  "date_joined": "2025-01-19T09:30:00Z",
  "last_login": "2025-01-19T10:30:00Z"
}
```

### 5. Avatar Yükleme

#### Endpoint
```
POST /upload-avatar/
```

#### Headers
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

#### Request Body (Form Data)
```
avatar: [file] (JPEG, PNG, GIF - Max 5MB)
```

#### Response
```json
{
  "success": true,
  "message": "Avatar başarıyla yüklendi",
  "user": {
    "id": 1,
    "email": "emrah.sander@uisoft.tech",
    "first_name": "Emrah",
    "last_name": "SANDER",
    "full_name": "Emrah SANDER",
    "phone": "+905551234567",
    "avatar": "http://localhost:8001/media/avatars/new_avatar.jpg",
    "avatar_url": "http://localhost:8001/media/avatars/new_avatar.jpg",
    "is_active": true,
    "is_verified": true,
    "date_joined": "2025-01-19T09:30:00Z",
    "last_login": "2025-01-19T10:30:00Z"
  }
}
```

### 6. Avatar Silme

#### Endpoint
```
DELETE /delete-avatar/
```

#### Headers
```
Authorization: Bearer <access_token>
```

#### Response
```json
{
  "success": true,
  "message": "Avatar başarıyla silindi",
  "user": {
    "id": 1,
    "email": "emrah.sander@uisoft.tech",
    "first_name": "Emrah",
    "last_name": "SANDER",
    "full_name": "Emrah SANDER",
    "phone": "+905551234567",
    "avatar": null,
    "avatar_url": null,
    "is_active": true,
    "is_verified": true,
    "date_joined": "2025-01-19T09:30:00Z",
    "last_login": "2025-01-19T10:30:00Z"
  }
}
```

---

## 💰 Tahsilat Modülü

### Base URL
```
https://your-domain.com/api/v1/tahsilat/
```

### 1. Tahsilat Sorgusu

#### Endpoint
```
POST /sorgu/
```

#### Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

#### Request Body
```json
{
  "tckn": "12345678901",  // TC Kimlik No (opsiyonel)
  "vkn": "1620052379",    // Vergi Kimlik No (opsiyonel)
  "baslangic_tarihi": "2024-01-01T00:00:00Z",  // Opsiyonel
  "bitis_tarihi": "2024-12-31T23:59:59Z",      // Opsiyonel
  "sadece_odenmemis": true  // Sadece ödenmemiş kayıtlar
}
```

#### Response (Başarılı)
```json
{
  "sorgu_id": 3,
  "basarili": true,
  "tahsilat_kayitlari": [
    {
      "id": 2,
      "tahsilat_id": 1228,
      "tahakkuk_no": "20211180800000063",
      "gelir_turu": "08 - İçme Kullanma ve Endüstri Suyu Tesislerine İlişkin Yatırım Bedeli Geri Ödeme Gelirleri",
      "borcun_konusu": " 63550 nolu sondaj kuyusu yatırım geri ödemesi",
      "cari_id": 1792,
      "ana_para_borc": "119876.49",
      "yapilan_toplam_tahsilat": "46521.11",
      "kalan_anapara_borc": "73355.38",
      "tahakkuk_donemi": null,
      "harici_id": 12364,
      "odeme_durumu": "Kısmi Ödendi",
      "kullanici_adi": "Emrah SANDER",
      "sorgu_tarihi": "2025-09-19T12:58:06.038360+03:00",
      "son_guncelleme": "2025-09-19T12:58:06.038494+03:00",
      "aktif": true
    }
  ],
  "ozet": {
    "ana_para_borc": "1474698.61",
    "yapilan_toplam_tahsilat": "554320.86",
    "toplam_kalan_anapara_borc": "920377.75",
    "sonuc_kodu": "001",
    "sonuc_aciklamasi": "İşlem başarılıdır."
  },
  "mesaj": "2 adet tahsilat kaydı bulundu"
}
```

### 2. Tahsilat Listesi

#### Endpoint
```
GET /liste/
```

#### Headers
```
Authorization: Bearer <access_token>
```

#### Query Parameters
```
?page=1&page_size=20&odeme_durumu=Kısmi Ödendi
```

#### Response
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 3,
      "tahsilat_id": 226959,
      "tahakkuk_no": "20241180800000103",
      "gelir_turu": "08 - İçme Kullanma ve Endüstri Suyu Tesislerine İlişkin Yatırım Bedeli Geri Ödeme Gelirleri",
      "borcun_konusu": "İhsaniye-Gazlıgöl İçmesuyu Arsenik Arıtma Tesisi (2.Aşama) yatırım geri ödemesi",
      "cari_id": 1792,
      "ana_para_borc": "1354822.12",
      "yapilan_toplam_tahsilat": "507799.75",
      "kalan_anapara_borc": "847022.37",
      "tahakkuk_donemi": null,
      "harici_id": 94467,
      "odeme_durumu": "Kısmi Ödendi",
      "kullanici_adi": "Emrah SANDER",
      "sorgu_tarihi": "2025-09-19T12:58:06.040026+03:00",
      "son_guncelleme": "2025-09-19T12:58:06.040106+03:00",
      "aktif": true
    }
  ]
}
```

### 3. Tahsilat Detayı

#### Endpoint
```
GET /detay-getir/{tahsilat_id}/
```

#### Headers
```
Authorization: Bearer <access_token>
```

#### Response
```json
{
  "success": true,
  "tahsilat_kaydi": {
    "id": 2,
    "tahsilat_id": 1228,
    "tahakkuk_no": "20211180800000063",
    "gelir_turu": "08 - İçme Kullanma ve Endüstri Suyu Tesislerine İlişkin Yatırım Bedeli Geri Ödeme Gelirleri",
    "borcun_konusu": " 63550 nolu sondaj kuyusu yatırım geri ödemesi",
    "cari_id": 1792,
    "ana_para_borc": "119876.49",
    "yapilan_toplam_tahsilat": "46521.11",
    "kalan_anapara_borc": "73355.38",
    "tahakkuk_donemi": null,
    "harici_id": 12364,
    "odeme_durumu": "Kısmi Ödendi",
    "kullanici_adi": "Emrah SANDER",
    "sorgu_tarihi": "2025-09-19T12:58:06.038360+03:00",
    "son_guncelleme": "2025-09-19T12:58:06.038494+03:00",
    "aktif": true
  },
  "detay_bilgileri": {
    "cariAd": "GAZLIGÖL BELEDİYE BAŞKANLIĞI",
    "tahakkukNo": "20211180800000063",
    "borcunKonusu": " 63550 nolu sondaj kuyusu yatırım geri ödemesi",
    "gelirTuru": "08 - İçme Kullanma ve Endüstri Suyu Tesislerine İlişkin Yatırım Bedeli Geri Ödeme Gelirleri",
    "tahsilatTaksitler": [
      {
        "tahsilatId": 1228,
        "vadeTarihi": "2016-04-30T00:00:00",
        "anaParaBorc": 3667.77,
        "kalanAnaParaBorc": 0.0,
        "kalanFaizBorc": 0.0,
        "kalanBorc": 0.0,
        "odenenAnaPara": 3667.77,
        "odenenFaizBorc": 0.0,
        "toplamOdenen": 3667.77,
        "id": 14158
      }
      // ... 30 yıllık taksit planı
    ],
    "tahsilatMahsupOdenenler": [
      {
        "tahsilatId": 1228,
        "mahsupTarihi": "2022-03-14T00:00:00",
        "toplamOdenenTutar": 8464.08,
        "anaParaOdenenTutar": 8464.08,
        "faizOdenenTutar": 0.0,
        "mahsupSiraNo": 0,
        "id": 0
      }
      // ... ödeme geçmişi
    ],
    "toplamOdenenAnapara": 46521.11,
    "toplamOdenenFaiz": 0.0,
    "toplamKalanAnapara": 73355.38,
    "toplamOdenenTutar": 46521.11,
    "toplamAnapara": 119876.49,
    "toplamFaiz": 0.0,
    "sonucBilgisi": {
      "sonucKodu": "001",
      "sonucAciklamasi": "İşlem başarılıdır."
    }
  },
  "message": "Tahsilat detay bilgileri başarıyla getirildi"
}
```

### 4. Tahsilat Belge Getir (PDF)

Tahsilat kaydının detay belgesini direkt PDF dosyası olarak getirir. **Public endpoint - authentication gerektirmez.**

#### Endpoint
```
GET /belge-getir/{tahsilat_id}/
```

#### Headers
```
# Authentication gerekmez - public endpoint
```

#### Response
Direkt PDF dosyası döndürülür. Content-Type: `application/pdf`

#### React Native Örneği
```javascript
const getTahsilatBelge = async (tahsilatId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/tahsilat/belge-getir/${tahsilatId}/`, {
      method: 'GET'
      // Authentication gerekmez - public endpoint
    });
    
    if (response.ok) {
      // PDF blob'u al
      const pdfBlob = await response.blob();
      
      // Blob'u URL'e çevir
      const pdfUrl = URL.createObjectURL(pdfBlob);
      
      // Dosya adını response header'ından al
      const contentDisposition = response.headers.get('Content-Disposition');
      const filename = contentDisposition 
        ? contentDisposition.split('filename=')[1].replace(/"/g, '')
        : `tahsilat_${tahsilatId}.pdf`;
      
      return {
        pdfUrl: pdfUrl,
        filename: filename,
        blob: pdfBlob
      };
    } else {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Tahsilat belgesi getirilemedi');
    }
  } catch (error) {
    console.error('Tahsilat belge hatası:', error);
    throw error;
  }
};

// PDF'i görüntüleme (Expo)
const viewTahsilatBelge = async (tahsilatId) => {
  try {
    const { pdfUrl, filename } = await getTahsilatBelge(tahsilatId);
    
    // Expo WebBrowser ile açma
    import * as WebBrowser from 'expo-web-browser';
    await WebBrowser.openBrowserAsync(pdfUrl);
    
  } catch (error) {
    console.error('PDF görüntüleme hatası:', error);
  }
};

// PDF'i dosya olarak kaydetme (Expo)
const saveTahsilatBelge = async (tahsilatId) => {
  try {
    const { blob, filename } = await getTahsilatBelge(tahsilatId);
    
    // Expo FileSystem kullanarak kaydetme
    import * as FileSystem from 'expo-file-system';
    
    const fileUri = `${FileSystem.documentDirectory}${filename}`;
    const base64 = await blobToBase64(blob);
    
    await FileSystem.writeAsStringAsync(fileUri, base64, {
      encoding: FileSystem.EncodingType.Base64,
    });
    
    console.log('PDF dosyası kaydedildi:', fileUri);
    return fileUri;
  } catch (error) {
    console.error('PDF kaydetme hatası:', error);
    throw error;
  }
};

// Blob'u base64'e çevirme yardımcı fonksiyon
const blobToBase64 = (blob) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result.split(',')[1]);
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
};

// React Native PDF görüntüleyici ile açma (react-native-pdf kütüphanesi)
const openPdfViewer = async (tahsilatId) => {
  try {
    const { pdfUrl } = await getTahsilatBelge(tahsilatId);
    
    // react-native-pdf kütüphanesi kullanarak
    import Pdf from 'react-native-pdf';
    
    // PDF component'ini render et
    return (
      <Pdf
        source={{ uri: pdfUrl }}
        onLoadComplete={(numberOfPages, filePath) => {
          console.log(`PDF yüklendi: ${numberOfPages} sayfa`);
        }}
        onPageChanged={(page, numberOfPages) => {
          console.log(`Sayfa ${page} / ${numberOfPages}`);
        }}
        onError={(error) => {
          console.error('PDF hatası:', error);
        }}
        style={{ flex: 1 }}
      />
    );
  } catch (error) {
    console.error('PDF görüntüleyici hatası:', error);
  }
};
```

### 5. Tahsilat İstatistikleri

#### Endpoint
```
GET /istatistikler/
```

#### Headers
```
Authorization: Bearer <access_token>
```

#### Response
```json
{
  "toplam_borc": {
    "toplam_ana_para": "1474698.61",
    "toplam_yapilan_tahsilat": "554320.86",
    "toplam_kalan_borc": "920377.75"
  },
  "odeme_durumlari": {
    "odendi": 0,
    "ksmi_odendi": 2,
    "odenmedi": 0
  },
  "sorgu_istatistikleri": {
    "toplam_sorgu": 3,
    "basarili_sorgu": 2,
    "basarisiz_sorgu": 1
  }
}
```

### 5. Tahsilat Kaydını Yenile

#### Endpoint
```
POST /yenile/{tahsilat_id}/
```

#### Headers
```
Authorization: Bearer <access_token>
```

#### Response
```json
{
  "success": true,
  "message": "Tahsilat kaydı başarıyla yenilendi",
  "tahsilat_kaydi": {
    // Güncellenmiş tahsilat kaydı
  }
}
```

---

## 📢 Duyurular Modülü

### Base URL
```
https://your-domain.com/api/v1/duyurular/
```

### 1. Duyuru Listesi

#### Endpoint
```
GET /liste/
```

#### Headers
```
# Public endpoint - authentication gerekmez
```

#### Query Parameters
```
?kategori=Teknoloji&tip=onemli&arama=mobil&page=1&page_size=20
```

#### Response
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "baslik": "Yeni Mobil Uygulama",
      "kategori": "Teknoloji",
      "tip": "onemli",
      "tip_renk": "#dc3545",
      "tip_etiket": "ÖNEMLİ",
      "ozet": "DSİ mobil uygulaması yayında",
      "resim_url": "https://your-domain.com/media/duyurular/resimler/duyuru1.jpg",
      "tarih": "2025-09-14T15:16:05.528794+03:00",
      "yayinlandi": true,
      "sira": 1
    }
  ]
}
```

### 2. Duyuru Detayı

#### Endpoint
```
GET /detay/{id}/
```

#### Headers
```
# Public endpoint - authentication gerekmez
```

#### Response
```json
{
  "id": 1,
  "baslik": "Yeni Mobil Uygulama",
  "kategori": "Teknoloji",
  "tip": "onemli",
  "tip_renk": "#dc3545",
  "tip_etiket": "ÖNEMLİ",
  "ozet": "DSİ mobil uygulaması yayında",
  "detaylar": "Yeni mobil uygulamamız ile tüm hizmetlere kolayca erişebilirsiniz. Tahsilat sorgulama, duyuru takibi ve daha birçok özellik artık cebinizde.",
  "resim": null,
  "resim_url": "https://your-domain.com/media/duyurular/resimler/duyuru1.jpg",
  "tarih": "2025-09-14T15:16:05.528794+03:00",
  "olusturma_tarihi": "2025-09-19T15:16:05.528945+03:00",
  "guncelleme_tarihi": "2025-09-19T15:16:05.528948+03:00",
  "aktif": true,
  "yayinlandi": true,
  "sira": 1
}
```

### 3. Duyuru Kategorileri

#### Endpoint
```
GET /kategoriler/
```

#### Headers
```
# Public endpoint - authentication gerekmez
```

#### Response
```json
{
  "success": true,
  "kategoriler": [
    "Teknoloji",
    "Sistem",
    "Güncelleme",
    "Anket",
    "Güvenlik"
  ]
}
```

### 4. Duyuru Tipleri

#### Endpoint
```
GET /tipler/
```

#### Headers
```
# Public endpoint - authentication gerekmez
```

#### Response
```json
{
  "success": true,
  "tipler": [
    {
      "value": "normal",
      "label": "Normal",
      "renk": "#28a745"
    },
    {
      "value": "onemli",
      "label": "Önemli",
      "renk": "#dc3545"
    },
    {
      "value": "acil",
      "label": "Acil",
      "renk": "#ffc107"
    },
    {
      "value": "bilgi",
      "label": "Bilgi",
      "renk": "#17a2b8"
    }
  ]
}
```

### 5. Duyuru İstatistikleri

#### Endpoint
```
GET /istatistikler/
```

#### Headers
```
# Public endpoint - authentication gerekmez
```

#### Response
```json
{
  "success": true,
  "istatistikler": {
    "toplam_duyuru": 5,
    "yayinlanan_duyuru": 5,
    "bekleyen_duyuru": 0,
    "kategori_sayilari": {
      "Teknoloji": 1,
      "Sistem": 1,
      "Güncelleme": 1,
      "Anket": 1,
      "Güvenlik": 1
    },
    "tip_sayilari": {
      "normal": 1,
      "onemli": 2,
      "acil": 1,
      "bilgi": 1
    }
  }
}
```

### 6. Duyuru Oluşturma (Admin)

#### Endpoint
```
POST /olustur/
```

#### Headers
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

#### Request Body (Form Data)
```
baslik: "Yeni Duyuru Başlığı"
kategori: "Teknoloji"
tip: "onemli"
ozet: "Duyuru özeti"
detaylar: "Detaylı duyuru içeriği"
resim: [file] (opsiyonel)
tarih: "2025-09-19T15:16:05Z" (opsiyonel)
aktif: true
yayinlandi: false
sira: 1
```

### 7. Duyuru Güncelleme (Admin)

#### Endpoint
```
PUT /guncelle/{id}/
```

#### Headers
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

### 8. Duyuru Silme (Admin)

#### Endpoint
```
DELETE /sil/{id}/
```

#### Headers
```
Authorization: Bearer <access_token>
```

### 9. Duyuru Yayınla/Yayından Kaldır (Admin)

#### Endpoint
```
POST /yayinla/{duyuru_id}/
```

#### Headers
```
Authorization: Bearer <access_token>
```

#### Response
```json
{
  "success": true,
  "message": "Duyuru yayınlandı",
  "yayinlandi": true
}
```

### React Native Örnekleri

#### Duyuru Listesi Getirme
```javascript
const getDuyuruList = async (filters = {}) => {
  try {
    const params = new URLSearchParams();
    
    if (filters.kategori) params.append('kategori', filters.kategori);
    if (filters.tip) params.append('tip', filters.tip);
    if (filters.arama) params.append('arama', filters.arama);
    if (filters.page) params.append('page', filters.page);
    if (filters.page_size) params.append('page_size', filters.page_size);
    
    const response = await fetch(`${API_BASE_URL}/api/v1/duyurular/liste/?${params}`);
    const data = await response.json();
    
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error.message };
  }
};
```

#### Duyuru Detayı Getirme
```javascript
const getDuyuruDetail = async (duyuruId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/duyurular/detay/${duyuruId}/`);
    const data = await response.json();
    
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error.message };
  }
};
```

#### Duyuru Kategorileri Getirme
```javascript
const getDuyuruKategorileri = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/duyurular/kategoriler/`);
    const data = await response.json();
    
    return { success: true, kategoriler: data.kategoriler };
  } catch (error) {
    return { success: false, error: error.message };
  }
};
```

#### Duyuru Tipleri Getirme
```javascript
const getDuyuruTipleri = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/duyurular/tipler/`);
    const data = await response.json();
    
    return { success: true, tipler: data.tipleri };
  } catch (error) {
    return { success: false, error: error.message };
  }
};
```

#### Duyuru Oluşturma (Admin)
```javascript
const createDuyuru = async (duyuruData, token) => {
  try {
    const formData = new FormData();
    
    formData.append('baslik', duyuruData.baslik);
    formData.append('kategori', duyuruData.kategori);
    formData.append('tip', duyuruData.tip);
    formData.append('ozet', duyuruData.ozet);
    formData.append('detaylar', duyuruData.detaylar);
    formData.append('aktif', duyuruData.aktif);
    formData.append('yayinlandi', duyuruData.yayinlandi);
    formData.append('sira', duyuruData.sira);
    
    if (duyuruData.resim) {
      formData.append('resim', {
        uri: duyuruData.resim.uri,
        type: duyuruData.resim.type,
        name: duyuruData.resim.name
      });
    }
    
    if (duyuruData.tarih) {
      formData.append('tarih', duyuruData.tarih);
    }
    
    const response = await fetch(`${API_BASE_URL}/api/v1/duyurular/olustur/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'multipart/form-data',
      },
      body: formData
    });
    
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error.message };
  }
};
```

#### Duyuru Yayınla/Yayından Kaldır (Admin)
```javascript
const toggleDuyuruYayin = async (duyuruId, token) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/duyurular/yayinla/${duyuruId}/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      }
    });
    
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error.message };
  }
};
```

#### Duyuru Kartı Komponenti Örneği
```javascript
import React from 'react';
import { View, Text, Image, TouchableOpacity, StyleSheet } from 'react-native';

const DuyuruKarti = ({ duyuru, onPress }) => {
  return (
    <TouchableOpacity style={styles.kart} onPress={() => onPress(duyuru)}>
      {/* Resim */}
      {duyuru.resim_url && (
        <Image source={{ uri: duyuru.resim_url }} style={styles.resim} />
      )}
      
      {/* Tip Etiketi */}
      <View style={[styles.tipEtiket, { backgroundColor: duyuru.tip_renk }]}>
        <Text style={styles.tipText}>{duyuru.tip_etiket}</Text>
      </View>
      
      {/* Kategori ve Tarih */}
      <View style={styles.ustBilgi}>
        <Text style={styles.kategori}>{duyuru.kategori}</Text>
        <Text style={styles.tarih}>
          {new Date(duyuru.tarih).toLocaleDateString('tr-TR')}
        </Text>
      </View>
      
      {/* Başlık */}
      <Text style={styles.baslik}>{duyuru.baslik}</Text>
      
      {/* Özet */}
      <Text style={styles.ozet}>{duyuru.ozet}</Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  kart: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 16,
    marginVertical: 8,
    marginHorizontal: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  resim: {
    width: '100%',
    height: 200,
    borderRadius: 8,
    marginBottom: 12,
  },
  tipEtiket: {
    position: 'absolute',
    top: 20,
    left: 20,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  tipText: {
    color: 'white',
    fontSize: 12,
    fontWeight: 'bold',
  },
  ustBilgi: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  kategori: {
    fontSize: 14,
    color: '#666',
  },
  tarih: {
    fontSize: 14,
    color: '#666',
  },
  baslik: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  ozet: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
});

export default DuyuruKarti;
```

#### Duyuru Detay Sayfası Örneği
```javascript
import React from 'react';
import { View, Text, Image, ScrollView, StyleSheet } from 'react-native';

const DuyuruDetay = ({ duyuru }) => {
  return (
    <ScrollView style={styles.container}>
      {/* Resim */}
      {duyuru.resim_url && (
        <Image source={{ uri: duyuru.resim_url }} style={styles.resim} />
      )}
      
      {/* Tip Etiketi */}
      <View style={[styles.tipEtiket, { backgroundColor: duyuru.tip_renk }]}>
        <Text style={styles.tipText}>{duyuru.tip_etiket}</Text>
      </View>
      
      {/* Kategori ve Tarih */}
      <View style={styles.ustBilgi}>
        <Text style={styles.kategori}>{duyuru.kategori}</Text>
        <Text style={styles.tarih}>
          {new Date(duyuru.tarih).toLocaleDateString('tr-TR')}
        </Text>
      </View>
      
      {/* Başlık */}
      <Text style={styles.baslik}>{duyuru.baslik}</Text>
      
      {/* Özet */}
      <View style={styles.ozetBolumu}>
        <Text style={styles.ozetBaslik}>Özet</Text>
        <View style={styles.cizgi} />
        <Text style={styles.ozet}>{duyuru.ozet}</Text>
      </View>
      
      {/* Detaylar */}
      <View style={styles.detayBolumu}>
        <Text style={styles.detayBaslik}>Detaylar</Text>
        <View style={styles.cizgi} />
        <Text style={styles.detaylar}>{duyuru.detaylar}</Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  resim: {
    width: '100%',
    height: 250,
  },
  tipEtiket: {
    position: 'absolute',
    top: 20,
    left: 20,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
  },
  tipText: {
    color: 'white',
    fontSize: 14,
    fontWeight: 'bold',
  },
  ustBilgi: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 20,
    paddingTop: 10,
  },
  kategori: {
    fontSize: 16,
    color: '#666',
  },
  tarih: {
    fontSize: 16,
    color: '#666',
  },
  baslik: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    paddingHorizontal: 20,
    marginBottom: 20,
  },
  ozetBolumu: {
    backgroundColor: 'white',
    margin: 20,
    padding: 20,
    borderRadius: 12,
  },
  ozetBaslik: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#28a745',
    marginBottom: 8,
  },
  cizgi: {
    height: 1,
    backgroundColor: '#ddd',
    marginBottom: 12,
  },
  ozet: {
    fontSize: 16,
    color: '#666',
    lineHeight: 24,
  },
  detayBolumu: {
    backgroundColor: 'white',
    margin: 20,
    padding: 20,
    borderRadius: 12,
  },
  detayBaslik: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#28a745',
    marginBottom: 8,
  },
  detaylar: {
    fontSize: 16,
    color: '#666',
    lineHeight: 24,
  },
});

export default DuyuruDetay;
```

---

## ⚠️ Hata Yönetimi

### HTTP Status Kodları

- **200 OK**: İşlem başarılı
- **201 Created**: Kayıt oluşturuldu
- **400 Bad Request**: Geçersiz istek
- **401 Unauthorized**: Kimlik doğrulama gerekli
- **403 Forbidden**: Yetkisiz erişim
- **404 Not Found**: Kaynak bulunamadı
- **500 Internal Server Error**: Sunucu hatası

### Hata Response Formatı

```json
{
  "error": "Hata mesajı",
  "detail": "Detaylı hata açıklaması",
  "code": "ERROR_CODE"
}
```

### Yaygın Hata Mesajları

- **Kimlik Doğrulama:**
  - `"Geçersiz kullanıcı adı veya şifre"`
  - `"Hesap devre dışı veya yetkisiz"`
  - `"Token geçersiz veya süresi geçmiş"`

- **Tahsilat:**
  - `"DSİ API bağlantı hatası"`
  - `"Tahsilat kaydı bulunamadı"`
  - `"Geçersiz TCKN veya VKN"`

---

## 💻 Örnek Kodlar

### React Native - Axios ile API Çağrısı

```javascript
import axios from 'axios';

const API_BASE_URL = 'https://your-domain.com/api/v1';

// Axios instance oluştur
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

// Request interceptor - Token ekle
api.interceptors.request.use(
  (config) => {
    const token = AsyncStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - Token yenileme
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token yenile
      try {
        const refreshToken = await AsyncStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
          refresh: refreshToken
        });
        
        await AsyncStorage.setItem('access_token', response.data.access);
        // Orijinal isteği tekrar dene
        return api.request(error.config);
      } catch (refreshError) {
        // Login sayfasına yönlendir
        navigation.navigate('Login');
      }
    }
    return Promise.reject(error);
  }
);
```

### Giriş Yapma

```javascript
const login = async (usernameOrEmail, password) => {
  try {
    const response = await api.post('/auth/external-login/', {
      usernameOrEmail,
      password
    });
    
    const { access, refresh, user } = response.data;
    
    // Token'ları sakla
    await AsyncStorage.setItem('access_token', access);
    await AsyncStorage.setItem('refresh_token', refresh);
    await AsyncStorage.setItem('user', JSON.stringify(user));
    
    return { success: true, user };
  } catch (error) {
    return { 
      success: false, 
      error: error.response?.data?.error || 'Giriş yapılamadı' 
    };
  }
};
```

### Profil Bilgileri Getirme

```javascript
const getProfile = async () => {
  try {
    const response = await api.get('/users/profile/');
    return { success: true, data: response.data };
  } catch (error) {
    return { 
      success: false, 
      error: error.response?.data?.error || 'Profil bilgileri alınamadı' 
    };
  }
};
```

### Profil Güncelleme

```javascript
const updateProfile = async (profileData) => {
  try {
    const response = await api.patch('/users/update-profile/', profileData);
    return { success: true, data: response.data };
  } catch (error) {
    return { 
      success: false, 
      error: error.response?.data?.error || 'Profil güncellenemedi' 
    };
  }
};
```

### Avatar Yükleme

```javascript
const uploadAvatar = async (imageUri) => {
  try {
    const formData = new FormData();
    
    formData.append('avatar', {
      uri: imageUri,
      type: 'image/jpeg', // veya 'image/png'
      name: 'avatar.jpg'
    });
    
    const response = await fetch(`${API_BASE_URL}/api/v1/users/upload-avatar/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${await AsyncStorage.getItem('access_token')}`,
        'Content-Type': 'multipart/form-data',
      },
      body: formData
    });
    
    const data = await response.json();
    
    if (data.success) {
      return { success: true, user: data.user };
    } else {
      return { success: false, error: data.errors || 'Avatar yüklenemedi' };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
};
```

### Avatar Silme

```javascript
const deleteAvatar = async () => {
  try {
    const response = await api.delete('/users/delete-avatar/');
    return { success: true, data: response.data };
  } catch (error) {
    return { 
      success: false, 
      error: error.response?.data?.error || 'Avatar silinemedi' 
    };
  }
};
```

### Profil Komponenti Örneği

```javascript
import React, { useState, useEffect } from 'react';
import { View, Text, Image, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import * as ImagePicker from 'expo-image-picker';

const ProfileScreen = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    const result = await getProfile();
    if (result.success) {
      setUser(result.data);
    }
    setLoading(false);
  };

  const handleImagePicker = async () => {
    try {
      // İzin iste
      const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();
      
      if (permissionResult.granted === false) {
        Alert.alert('Hata', 'Galeri erişim izni gerekli');
        return;
      }

      // Resim seç
      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [1, 1],
        quality: 0.8,
      });

      if (!result.canceled) {
        await uploadAvatar(result.assets[0].uri);
        loadProfile(); // Profili yenile
      }
    } catch (error) {
      Alert.alert('Hata', 'Resim seçilirken bir hata oluştu');
    }
  };

  const handleDeleteAvatar = async () => {
    Alert.alert(
      'Avatar Sil',
      'Avatarınızı silmek istediğinizden emin misiniz?',
      [
        { text: 'İptal', style: 'cancel' },
        { 
          text: 'Sil', 
          style: 'destructive',
          onPress: async () => {
            const result = await deleteAvatar();
            if (result.success) {
              loadProfile(); // Profili yenile
            } else {
              Alert.alert('Hata', result.error);
            }
          }
        }
      ]
    );
  };

  if (loading) {
    return (
      <View style={styles.container}>
        <Text>Yükleniyor...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.avatarContainer}>
        {user?.avatar_url ? (
          <Image source={{ uri: user.avatar_url }} style={styles.avatar} />
        ) : (
          <View style={styles.avatarPlaceholder}>
            <Text style={styles.avatarText}>
              {user?.first_name?.[0]}{user?.last_name?.[0]}
            </Text>
          </View>
        )}
        
        <TouchableOpacity style={styles.avatarButton} onPress={handleImagePicker}>
          <Text style={styles.avatarButtonText}>Resim Değiştir</Text>
        </TouchableOpacity>
        
        {user?.avatar_url && (
          <TouchableOpacity style={styles.deleteButton} onPress={handleDeleteAvatar}>
            <Text style={styles.deleteButtonText}>Avatar Sil</Text>
          </TouchableOpacity>
        )}
      </View>
      
      <View style={styles.userInfo}>
        <Text style={styles.name}>{user?.full_name}</Text>
        <Text style={styles.email}>{user?.email}</Text>
        <Text style={styles.phone}>{user?.phone || 'Telefon yok'}</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  avatarContainer: {
    alignItems: 'center',
    marginBottom: 30,
  },
  avatar: {
    width: 120,
    height: 120,
    borderRadius: 60,
    marginBottom: 15,
  },
  avatarPlaceholder: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: '#ddd',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 15,
  },
  avatarText: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#666',
  },
  avatarButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
    marginBottom: 10,
  },
  avatarButtonText: {
    color: 'white',
    fontWeight: 'bold',
  },
  deleteButton: {
    backgroundColor: '#FF3B30',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
  },
  deleteButtonText: {
    color: 'white',
    fontWeight: 'bold',
  },
  userInfo: {
    alignItems: 'center',
  },
  name: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  email: {
    fontSize: 16,
    color: '#666',
    marginBottom: 5,
  },
  phone: {
    fontSize: 16,
    color: '#666',
  },
});

export default ProfileScreen;
```

### Tahsilat Sorgusu

```javascript
const searchTahsilat = async (searchParams) => {
  try {
    const response = await api.post('/tahsilat/sorgu/', searchParams);
    return { success: true, data: response.data };
  } catch (error) {
    return { 
      success: false, 
      error: error.response?.data?.error || 'Sorgu yapılamadı' 
    };
  }
};

// Kullanım
const result = await searchTahsilat({
  vkn: '1620052379',
  sadece_odenmemis: true
});
```

### Tahsilat Listesi

```javascript
const getTahsilatList = async (page = 1, pageSize = 20) => {
  try {
    const response = await api.get('/tahsilat/liste/', {
      params: { page, page_size: pageSize }
    });
    return { success: true, data: response.data };
  } catch (error) {
    return { 
      success: false, 
      error: error.response?.data?.error || 'Liste alınamadı' 
    };
  }
};
```

### Tahsilat Detayı

```javascript
const getTahsilatDetail = async (tahsilatId) => {
  try {
    const response = await api.get(`/tahsilat/detay-getir/${tahsilatId}/`);
    return { success: true, data: response.data };
  } catch (error) {
    return { 
      success: false, 
      error: error.response?.data?.error || 'Detay alınamadı' 
    };
  }
};
```

### Tahsilat İstatistikleri

```javascript
const getTahsilatStats = async () => {
  try {
    const response = await api.get('/tahsilat/istatistikler/');
    return { success: true, data: response.data };
  } catch (error) {
    return { 
      success: false, 
      error: error.response?.data?.error || 'İstatistikler alınamadı' 
    };
  }
};
```

---

## 🔧 Konfigürasyon

### Environment Variables

```javascript
// .env
API_BASE_URL=https://your-domain.com/api/v1
API_TIMEOUT=30000
```

### CORS Ayarları

Backend'de CORS ayarları yapılandırılmıştır. React Native uygulaması için ek CORS ayarı gerekmez.

---

## 📱 React Native Önerileri

1. **State Management**: Redux Toolkit veya Zustand kullanın
2. **Caching**: React Query veya SWR kullanın
3. **Error Handling**: Global error boundary oluşturun
4. **Loading States**: Skeleton loader kullanın
5. **Offline Support**: NetInfo ile offline durumu kontrol edin
6. **Security**: Token'ları SecureStore'da saklayın

---

## 🚀 Deployment

### Production URL
```
https://your-production-domain.com/api/v1/
```

### SSL Sertifikası
Tüm API çağrıları HTTPS üzerinden yapılmalıdır.

---

Bu dokümantasyon, frontend geliştirme sürecinde referans olarak kullanılabilir. Herhangi bir sorunuz olursa backend ekibi ile iletişime geçebilirsiniz.
