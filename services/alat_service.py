from models.alat import (Kondisi_Baik, Status_Dipinjam, Status_Pemeliharaan, Status_Rusak,
                         Status_Tersedia, Alat)
from models.exceptions import AturanBisnisError, DataSudahAdaError, DataTidakDitemukanError, ValidasiError
from utils.validasi import wajib_isi as wajib

KATEGORI_AWAL = ("perangkat komputasi", "perangkat jaringan", "perangkat multimedia")


class AlatService:
    """CRUD alat + pencarian + pemeliharaan. Data: dict {kode: Alat}.

    Kategori disimpan di set sehingga kategori baru dapat ditambahkan saat
    program berjalan tanpa mengubah kode/struktur class.
    """

    def __init__(self, log):
        self._data = {}
        self._kategori = set(KATEGORI_AWAL)
        self._log = log

    # ---- kategori ----
    def daftar_kategori(self):
        return sorted(self._kategori)

    def tambah_kategori(self, nama):
        nama = wajib(nama, "Kategori").lower()
        if nama in self._kategori:
            raise DataSudahAdaError(f"Kategori '{nama}' sudah ada.")
        self._kategori.add(nama)
        self._log.catat(f"Kategori '{nama}' ditambahkan")
        return nama

    def tambah(self, kode, nama, kategori, kondisi=Kondisi_Baik):
        kode = wajib(kode, "Kode alat").upper()
        nama = wajib(nama, "Nama alat")
        kategori = wajib(kategori, "Kategori").lower()
        if kode in self._data:
            raise DataSudahAdaError(f"Kode alat {kode} sudah terdaftar.")
        self._kategori.add(kategori)
        self._data[kode] = Alat(kode, nama, kategori, kondisi)
        self._log.catat(f"Alat {kode} ({nama}) ditambahkan")
        return self._data[kode]

    def ambil(self, kode):
        alat = self._data.get(kode.strip().upper())
        if alat is None:
            raise DataTidakDitemukanError(f"Alat dengan kode {kode.strip().upper()} tidak ditemukan.")
        return alat

    def edit(self, kode, nama=None, kategori=None):
        alat = self.ambil(kode)
        if nama:
            alat.nama = wajib(nama, "Nama alat")
        if kategori:
            alat.kategori = wajib(kategori, "Kategori").lower()
            self._kategori.add(alat.kategori)
        self._log.catat(f"Alat {alat.kode} diubah")
        return alat

    def hapus(self, kode):
        """Aturan 6: alat yang masih ada di transaksi aktif tidak boleh dihapus."""
        alat = self.ambil(kode)
        if alat.status == Status_Dipinjam:
            raise AturanBisnisError(
                f"Alat {alat.kode} masih tercatat di transaksi aktif {alat.transaksi_aktif}; tidak dapat dihapus."
            )
        del self._data[alat.kode]
        self._log.catat(f"Alat {alat.kode} dihapus")

    # ---- pencarian (Tantangan A) ----
    def cari(self, keyword, berdasarkan="semua"):
        """berdasarkan: 'kode' | 'nama' | 'kategori' | 'semua'."""
        k = wajib(keyword, "Kata kunci").lower()
        hasil = []
        for a in self._data.values():
            cocok = {
                "kode": k == a.kode.lower(),
                "nama": k in a.nama.lower(),
                "kategori": k in a.kategori.lower(),
            }
            if berdasarkan == "semua":
                if any(cocok.values()):
                    hasil.append(a)
            elif berdasarkan in cocok:
                if cocok[berdasarkan]:
                    hasil.append(a)
            else:
                raise ValidasiError("Mode pencarian harus: kode, nama, kategori, atau semua.")
        return hasil

    # ---- daftar berdasarkan status ----
    def _filter(self, status):
        return [a for a in self._data.values() if a.status == status]

    def semua(self):
        return list(self._data.values())

    def daftar_tersedia(self):
        return self._filter(Status_Tersedia)

    def daftar_dipinjam(self):
        return self._filter(Status_Dipinjam)

    def daftar_rusak(self):
        return self._filter(Status_Rusak)

    def daftar_pemeliharaan(self):
        return self._filter(Status_Pemeliharaan)

    # ---- pemeliharaan (Tantangan C) ----
    def kirim_ke_pemeliharaan(self, kode):
        alat = self.ambil(kode)
        alat.kirim_ke_pemeliharaan()
        self._log.catat(f"Alat {alat.kode} dimasukkan ke daftar pemeliharaan")
        return alat

    def selesai_pemeliharaan(self, kode):
        alat = self.ambil(kode)
        alat.selesai_pemeliharaan()
        self._log.catat(f"Alat {alat.kode} selesai diperbaiki dan kembali tersedia")
        return alat