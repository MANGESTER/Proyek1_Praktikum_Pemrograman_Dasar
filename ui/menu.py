"""MenuCLI: hanya menangani input/output. Logika bisnis ada di services/."""
import data_contoh
from models.enums import KondisiAlat
from models.exceptions import LabError
from models.transaksi import MAKS_HARI
from utils.validasi import parse_angka, parse_tanggal

class MenuCLI:
    def __init__(self, mahasiswa_service, alat_service, transaksi_service, log_service, statistik_service):
        self.ms = mahasiswa_service
        self.als = alat_service
        self.ts = transaksi_service
        self.log = log_service
        self.stat = statistik_service
        self.menu = {
            "1": ("Kelola data mahasiswa", self.kelola_mahasiswa),
            "2": ("Kelola data alat", self.kelola_alat),
            "3": ("Buat transaksi peminjaman", self.buat_transaksi),
            "4": ("Tampilkan transaksi", self.tampil_transaksi),
            "5": ("Proses pengembalian alat", self.pengembalian),
            "6": ("Cari transaksi berdasarkan mahasiswa", self.cari_transaksi),
            "7": ("Tampilkan alat yang tersedia", lambda: self._cetak(self.als.tersedia())),
            "8": ("Tampilkan alat yang sedang dipinjam", lambda: self._cetak(self.als.dipinjam())),
            "9": ("Tampilkan alat yang rusak", lambda: self._cetak(self.als.rusak())),
            "10": ("Tampilkan riwayat peminjaman mahasiswa", self.riwayat),
            "11": ("[A] Cari alat (kode / nama / kategori)", self.cari_alat),
            "12": ("[B] Statistik peminjaman", self.statistik),
            "13": ("[C] Pemeliharaan alat", self.pemeliharaan),
            "14": ("[D] Log aktivitas", self.log.tampilkan),
            "15": ("Tampilkan transaksi terlambat", self.terlambat),
            "16": ("Muat data contoh", self.muat_contoh),
            "0": ("Keluar", None),
        }

    # ---------- helper I/O ----------
    @staticmethod
    def _input(label):
        return input(f"{label}: ").strip()

    @staticmethod
    def _cetak(daftar, kosong="(Tidak ada data)"):
        if not daftar:
            print(kosong)
        for item in daftar:
            print(item)

    def _pilih_kondisi(self, label="Kondisi (baik/rusak ringan/rusak berat)"):
        return KondisiAlat.dari_teks(self._input(label))

    # ---------- loop utama ----------
    def tampilkan_menu(self):
        print("\n=== SISTEM PEMINJAMAN PERALATAN LABORATORIUM ===")
        for kode, (judul, _) in self.menu.items():
            if kode != "0":
                print(f"{kode:>3}. {judul}")
        print("  0. Keluar")

    def jalankan(self):
        while True:
            self.tampilkan_menu()
            pilihan = self._input("Pilih menu")
            if pilihan == "0":
                print("Terima kasih.")
                break
            if pilihan not in self.menu:
                print("Menu tidak valid.")
                continue
            try:
                self.menu[pilihan][1]()
            except (LabError, ValueError) as e:
                print(f"Gagal: {e}")
            except (KeyboardInterrupt, EOFError):
                print("\nDibatalkan.")

    # ---------- mahasiswa ----------
    def kelola_mahasiswa(self):
        print("a. Tambah  b. Edit  c. Hapus  d. Cari  e. Tampilkan semua")
        p = self._input("Pilih").lower()
        if p == "a":
            m = self.ms.tambah(self._input("NIM"), self._input("Nama"), self._input("No HP"))
            print("Berhasil ditambahkan:", m)
        elif p == "b":
            nim = self._input("NIM")
            m = self.ms.edit(nim, self._input("Nama baru (kosong = tetap)") or None,
                             self._input("No HP baru (kosong = tetap)") or None)
            print("Berhasil diubah:", m)
        elif p == "c":
            self.ms.hapus(self._input("NIM"))
            print("Mahasiswa dihapus.")
        elif p == "d":
            self._cetak(self.ms.cari(self._input("Kata kunci (NIM/nama)")))
        elif p == "e":
            self._cetak(self.ms.semua())
        else:
            print("Pilihan tidak valid.")

    # ---------- alat ----------
    def kelola_alat(self):
        print("a. Tambah  b. Edit  c. Hapus  d. Cari  e. Tampilkan semua")
        p = self._input("Pilih").lower()
        if p == "a":
            kode, nama = self._input("Kode"), self._input("Nama")
            if self.als.kategori:
                print("Kategori yang ada:", ", ".join(k.nama for k in self.als.kategori.values()))
            kategori = self._input("Kategori (boleh kategori baru)")
            kondisi = KondisiAlat.dari_teks(self._input("Kondisi awal [baik]") or "baik")
            print("Berhasil ditambahkan:", self.als.tambah(kode, nama, kategori, kondisi))
        elif p == "b":
            kode = self._input("Kode")
            a = self.als.edit(kode, self._input("Nama baru (kosong = tetap)") or None,
                              self._input("Kategori baru (kosong = tetap)") or None)
            print("Berhasil diubah:", a)
        elif p == "c":
            self.als.hapus(self._input("Kode"))
            print("Alat dihapus.")
        elif p == "d":
            self.cari_alat()
        elif p == "e":
            self._cetak(self.als.semua())
        else:
            print("Pilihan tidak valid.")

    def cari_alat(self):
        self._cetak(self.als.cari(self._input("Kata kunci (kode/nama/kategori)")))

    # ---------- transaksi ----------
    def buat_transaksi(self):
        nim = self._input("NIM mahasiswa")
        kode = self._input("Kode alat (pisahkan dengan koma)").split(",")
        lama = parse_angka(self._input(f"Lama pinjam (1-{MAKS_HARI} hari) [{MAKS_HARI}]") or MAKS_HARI, "Lama pinjam")
        t = self.ts.buat_transaksi(nim, kode, lama)
        print("Transaksi berhasil dibuat:\n" + str(t))

    def tampil_transaksi(self):
        self._cetak(self.ts.semua(), "(Belum ada transaksi)")

    def pengembalian(self):
        t = self.ts.ambil(self._input("ID transaksi"))
        print(t)
        belum = [d.alat.kode for d in t.alat_belum_kembali()]
        print("Belum kembali:", ", ".join(belum) or "-")
        pengembalian = {}
        for kode in self._input("Kode alat yang dikembalikan (pisahkan koma)").split(","):
            kode = kode.strip()
            if kode:
                pengembalian[kode] = self._pilih_kondisi(f"Kondisi {kode} (baik/rusak ringan/rusak berat)")
        tgl = self._input("Tanggal kembali YYYY-MM-DD (kosong = hari ini)")
        t = self.ts.proses_pengembalian(t.id_transaksi, pengembalian, parse_tanggal(tgl) if tgl else None)
        print("Pengembalian diproses:\n" + str(t))

    def cari_transaksi(self):
        self._cetak(self.ts.cari_berdasarkan_mahasiswa(self._input("NIM / nama mahasiswa")))

    def riwayat(self):
        self._cetak(self.ts.riwayat_mahasiswa(self._input("NIM mahasiswa")), "(Belum ada riwayat)")

    def terlambat(self):
        self._cetak(self.ts.terlambat(), "(Tidak ada transaksi terlambat)")

    # ---------- tantangan ----------
    def statistik(self):
        r = self.stat.ringkasan()
        print("Alat paling sering dipinjam:")
        for alat, jml in r["alat_terpopuler"] or []:
            print(f"  {alat.kode} {alat.nama}: {jml}x")
        print("Mahasiswa paling sering meminjam:")
        for m, jml in r["mahasiswa_teraktif"] or []:
            print(f"  {m.nim} {m.nama}: {jml} transaksi")
        print(f"Transaksi selesai: {r['transaksi_selesai']}")
        print(f"Transaksi aktif  : {r['transaksi_aktif']}")

    def pemeliharaan(self):
        print("a. Kirim alat rusak ke pemeliharaan  b. Selesai diperbaiki  c. Lihat daftar")
        p = self._input("Pilih").lower()
        if p == "a":
            self.als.kirim_pemeliharaan(self._input("Kode alat"))
            print("Alat masuk daftar pemeliharaan.")
        elif p == "b":
            self.als.selesai_perbaikan(self._input("Kode alat"))
            print("Alat kembali tersedia.")
        elif p == "c":
            self._cetak(self.als.daftar_pemeliharaan(), "(Tidak ada alat dalam pemeliharaan)")
        else:
            print("Pilihan tidak valid.")

    def muat_contoh(self):
        n = data_contoh.muat(self.ms, self.als)
        print(f"{n} data contoh dimuat.")
