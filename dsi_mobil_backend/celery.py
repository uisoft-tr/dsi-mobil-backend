import os
from celery import Celery

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dsi_mobil_backend.settings')

app = Celery('dsi_mobil_backend')

# Celery yapılandırmasını Django settings'den yükle
app.config_from_object('django.conf:settings', namespace='CELERY')

# Tüm uygulamalardan task'ları otomatik keşfet
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
