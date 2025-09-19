"""
DSİ API mock data - Test amaçlı
"""

MOCK_TAHSILAT_RESPONSE = {
    "tahsilatListe": [
        {
            "tahsilatId": 1228,
            "tahakkukNo": "20211180800000063",
            "gelirTuru": "08 - İçme Kullanma ve Endüstri Suyu Tesislerine İlişkin Yatırım Bedeli Geri Ödeme Gelirleri",
            "borcunKonusu": " 63550 nolu sondaj kuyusu yatırım geri ödemesi",
            "cariId": 1792,
            "anaParaBorc": 92822.77,
            "yapilanToplamTahsilat": 15799.62,
            "kalanAnaparaBorc": 77023.15,
            "tahakkukDonemi": "2016-01-31T00:00:00",
            "id": 12364
        },
        {
            "tahsilatId": 1281,
            "tahakkukNo": "20211180800000013",
            "gelirTuru": "08 - İçme Kullanma ve Endüstri Suyu Tesislerine İlişkin Yatırım Bedeli Geri Ödeme Gelirleri",
            "borcunKonusu": "İhsaniye-Gazlıgöl İçmesuyu Arsenik Arıtma Tesisi (2.Aşama) yatırım geri ödemesi",
            "cariId": 1792,
            "anaParaBorc": 1123327.14,
            "yapilanToplamTahsilat": 175560.88,
            "kalanAnaparaBorc": 947766.26,
            "tahakkukDonemi": "2017-01-31T00:00:00",
            "id": 12710
        },
        {
            "tahsilatId": 222235,
            "tahakkukNo": "20241180800000045",
            "gelirTuru": "08 - İçme Kullanma ve Endüstri Suyu Tesislerine İlişkin Yatırım Bedeli Geri Ödeme Gelirleri",
            "borcunKonusu": "İhsaniye-Gazlıgöl İçmesuyu Arsenik Arıtma Tesisi (2.Aşama) 2023 yılı Taksidi Ek tahakkuku",
            "cariId": 1792,
            "anaParaBorc": 18271.14,
            "yapilanToplamTahsilat": 0,
            "kalanAnaparaBorc": 18271.14,
            "tahakkukDonemi": "2024-01-31T00:00:00",
            "id": 78260
        },
        {
            "tahsilatId": 226959,
            "tahakkukNo": "20241180800000103",
            "gelirTuru": "08 - İçme Kullanma ve Endüstri Suyu Tesislerine İlişkin Yatırım Bedeli Geri Ödeme Gelirleri",
            "borcunKonusu": "İhsaniye-Gazlıgöl İçmesuyu Arsenik Arıtma Tesisi (2.Aşama) yatırım geri ödemesi",
            "cariId": 1792,
            "anaParaBorc": 945962.31,
            "yapilanToplamTahsilat": 58605.54,
            "kalanAnaparaBorc": 887356.77,
            "tahakkukDonemi": "2017-01-31T00:00:00",
            "id": 94467
        }
    ],
    "anaParaBorc": 2180383.36,
    "yapilanToplamTahsilat": 249966.04,
    "toplamKalanAnaparaBorc": 1930417.32,
    "sonucBilgisi": {
        "sonucKodu": "001",
        "sonucAciklamasi": "İşlem başarılıdır."
    },
    "id": 0
}

MOCK_ABP_RESPONSE = {
    "result": MOCK_TAHSILAT_RESPONSE,
    "targetUrl": None,
    "success": True,
    "error": None,
    "unAuthorizedRequest": False,
    "__abp": True
}
