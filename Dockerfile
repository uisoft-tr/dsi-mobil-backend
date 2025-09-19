# Python 3.11 slim image kullan
FROM python:3.11-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem paketlerini güncelle ve gerekli paketleri yükle
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Static dosyalar için dizin oluştur
RUN mkdir -p staticfiles media logs

# Port 8000'i aç
EXPOSE 8000

# Django uygulamasını çalıştır
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "dsi_mobil_backend.wsgi:application"]
