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

class Transaksi:
    def __init__(self, id_transaksi, nim, daftar_kode, tanggal_pinjam, lama_hari=max_hari):
        self.id = id_transaksi
        self.nim = nim 
        self.items = {kode: DetailPinjam(kode) for kode in daftar_kode}
        self.tanggal_pinjam = tanggal_pinjam
        self.batas_kembali = tanggal_pinjam + timedelta(days=lama_hari)
        self.status = status_dipinjam

    @property
    def aktif(self):
        return self.status != status_selesai

    def belum_kembali(self):
        return [k for k, d in self.items.items() if not d.sudah_dikembalikan]