from datetime import timedelta
from models.alat import cek_kondisi
from models.exceptions import AturanBisnisError, DataTidakDitemukanError

status_dipinjam = 'Dipinjam'
status_sebagian = 'Hanya Sebagian yang Dikembalikan'
status_selesai = 'selesai'
max_hari = 7

class DetailPinjam:
    def __init__(self, kode_alat):
        self.kode_alat = kode_alat
        self.tanggal_kembali = None
        self.kondisi_kembali = None
        self.terlambar = False

    @property
    def sudah_dikembalikan(self):
        return self.tanggal_kembali is not None