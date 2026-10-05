from models.exceptions import AturanBisnisError, ValidasiError

Kondisi_Baik = 'Baik'
Kondisi_Rusak_Ringan = 'Rusak Ringan'
Kondisi_Rusak_Berat = 'Rusak Berat'
Kondisi_Valid = (Kondisi_Baik, Kondisi_Rusak_Ringan, Kondisi_Rusak_Berat)

Status_Tersedia = 'Tersedia'
Status_Dipinjam = 'Dipinjam'
Status_Rusak = 'Rusak'
Status_Pemeliharaan = 'Pemeliharaan'

def cek_kondisi(kondisi):
    if kondisi not in Kondisi_Valid:
        raise ValidasiError(f'Kondisi harus salah satu dari: {', '.join(Kondisi_Valid)}')
    return kondisi

class Alat:
    def __init__(self, kode, nama, kategori, kondisi=Kondisi_Baik):
        self.kode = kode
        self.nama = nama
        self.kategori = kategori 
        self.kondisi = cek_kondisi(kondisi)
        self.status = Status_Tersedia if kondisi == Kondisi_Baik else Status_Rusak 
        self.transaksi_aktif = None 

    @property
    def tersedia(self):
        return self.status == Status_Tersedia

    def pinjam(self, id_transaksi):
        if not self.tersedia:
            raise AturanBisnisError(f'Alat {self.kode}, ({self.nama}) Tidak Tersedia (status =: {self.status})')
        self.status = Status_Dipinjam
        self.transaksi_aktif = id_transaksi

    def kembalikan(self, kondisi):
        self.kondisi = cek_kondisi(kondisi)
        self.transaksi_aktif = None
        self.status = Status_Tersedia if kondisi == Kondisi_Baik else Status_Rusak

    def proses_pemeliharaan(self):