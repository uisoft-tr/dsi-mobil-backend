from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from duyurular.models import Duyuru, DuyuruTipi


class Command(BaseCommand):
    help = 'Örnek duyuru verilerini oluşturur'

    def handle(self, *args, **options):
        # Mevcut duyuruları temizle
        Duyuru.objects.all().delete()
        
        # Örnek duyurular
        duyurular = [
            {
                'baslik': 'Yeni Mobil Uygulama',
                'kategori': 'Teknoloji',
                'tip': DuyuruTipi.ONEMLI,
                'ozet': 'DSİ mobil uygulaması yayında',
                'detaylar': 'Yeni mobil uygulamamız ile tüm hizmetlere kolayca erişebilirsiniz. Tahsilat sorgulama, duyuru takibi ve daha birçok özellik artık cebinizde.',
                'tarih': timezone.now() - timedelta(days=5),
                'yayinlandi': True,
                'sira': 1
            },
            {
                'baslik': 'Sistem Bakımı',
                'kategori': 'Sistem',
                'tip': DuyuruTipi.ACIL,
                'ozet': 'Sistem bakımı nedeniyle hizmet kesintisi',
                'detaylar': '15 Ocak 2024 tarihinde 02:00-06:00 saatleri arasında sistem bakımı yapılacaktır. Bu süre zarfında hizmetlerimiz geçici olarak kesintiye uğrayacaktır.',
                'tarih': timezone.now() - timedelta(days=3),
                'yayinlandi': True,
                'sira': 2
            },
            {
                'baslik': 'Yeni Özellikler',
                'kategori': 'Güncelleme',
                'tip': DuyuruTipi.BILGI,
                'ozet': 'Mobil uygulamaya yeni özellikler eklendi',
                'detaylar': 'Mobil uygulamamıza yeni özellikler eklendi:\n- Push bildirimleri\n- Offline çalışma desteği\n- Gelişmiş arama\n- Koyu tema seçeneği',
                'tarih': timezone.now() - timedelta(days=1),
                'yayinlandi': True,
                'sira': 3
            },
            {
                'baslik': 'Kullanıcı Anketi',
                'kategori': 'Anket',
                'tip': DuyuruTipi.NORMAL,
                'ozet': 'Uygulama hakkında görüşlerinizi paylaşın',
                'detaylar': 'Uygulamamızı daha da geliştirmek için görüşlerinize ihtiyacımız var. Lütfen kısa anketimizi doldurun ve geri bildirimlerinizi bizimle paylaşın.',
                'tarih': timezone.now() - timedelta(hours=12),
                'yayinlandi': True,
                'sira': 4
            },
            {
                'baslik': 'Güvenlik Güncellemesi',
                'kategori': 'Güvenlik',
                'tip': DuyuruTipi.ONEMLI,
                'ozet': 'Güvenlik güncellemesi yapıldı',
                'detaylar': 'Hesap güvenliğinizi artırmak için yeni güvenlik önlemleri eklendi. Lütfen şifrenizi güncelleyin ve 2FA özelliğini aktifleştirin.',
                'tarih': timezone.now() - timedelta(hours=6),
                'yayinlandi': True,
                'sira': 5
            }
        ]
        
        # Duyuruları oluştur
        for duyuru_data in duyurular:
            Duyuru.objects.create(**duyuru_data)
        
        self.stdout.write(
            self.style.SUCCESS(f'{len(duyurular)} adet örnek duyuru oluşturuldu.')
        )
