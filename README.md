# Praktikum Pemrograman 

# Sistem Pengelolaan Peminjaman Peralatan Laboratorium

Aplikasi CLI berbasis Python (OOP, tanpa database) untuk mengelola mahasiswa, alat, peminjaman,
dan pengembalian alat laboratorium. Data disimpan sementara di `list`/`dict`/`set` selama program berjalan.

## Anggota Kelompok
| Nama | Peran utama |
|---|---|
| Mahardika | Model (`models/`), UML final |
| Abyan | `TransaksiService`, pengujian skenario peminjaman/pengembalian |
| Ayun | `MahasiswaService`, `AlatService`, Tantangan A & C |
| Adibah | `MenuCLI`, `main.py`, `LogService`, `StatistikService`, dokumentasi |

## Deskripsi Sistem
Mengatasi masalah pencatatan manual: ketersediaan alat, riwayat peminjaman, keterlambatan, dan kondisi alat setelah dikembalikan.
Aturan bisnis yang diterapkan:
1. Alat yang tidak tersedia tidak bisa dipinjam (transaksi ditolak seluruhnya / atomic).
2. Maks. 2 transaksi aktif per mahasiswa.
3. Satu transaksi dapat berisi banyak alat (`dict`), lama pinjam 1-7 hari.
4. Pengembalian sebagian diperbolehkan; transaksi `selesai` hanya bila semua alat kembali.
5. Hanya alat berkondisi **baik** yang kembali tersedia; rusak ringan/berat tidak.
6. Mahasiswa/alat yang masih ada di transaksi aktif tidak dapat dihapus.

Tantangan yang dikerjakan: **A** pencarian fleksibel, **B** statistik, **C** pemeliharaan, **D** log aktivitas.

## Struktur Program
lab_peminjaman/
├── main.py                  # titik masuk
├── data_contoh.py           # data contoh (menu 16)
├── models/                  # Mahasiswa, Alat, Transaksi, DetailPinjam, exceptions
├── services/                # MahasiswaService, AlatService, TransaksiService, LogService, StatistikService
├── ui/menu.py               # MenuCLI (hanya input/output)
├── utils/validasi.py
├── tests/test_skenario.py   # unit test skenario 1-6 + tantangan
└── docs/                    # UML, keputusan desain, pengujian, code review, refleksi, pembagian tugas

## Cara Menjalankan
Butuh Python 3.8+ (tanpa library tambahan).
```bash
python main.py                    # jalankan aplikasi (menu 16 = muat data contoh)
python -m unittest discover -v    # jalankan seluruh pengujian
```
## Pembagian Kontribusi
Lihat [`docs/pembagian_tugas.md`](docs/pembagian_tugas.md). Setiap anggota commit memakai akun GitHub masing-masing.

## Dokumentasi
`docs/uml_final.drawio` · `docs/uml_final.md` · `docs/desain_keputusan.md` · `docs/hasil_pengujian.md` · `docs/code_review.md` · `docs/refleksi.md`
