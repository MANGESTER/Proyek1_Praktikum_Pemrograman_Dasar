"""Tantangan B: statistik peminjaman."""
from collections import Counter
from models.enums import StatusTransaksi

class StatistikService:
    def __init__(self, transaksi_service):
        self.transaksi_service = transaksi_service

    def alat_terpopuler(self, n=3):
        c = Counter()
        for t in self.transaksi_service.semua():
            for d in t.detail.values():
                c[d.alat] += 1
        return [(alat, jml) for alat, jml in sorted(c.items(), key=lambda x: (-x[1], x[0].kode))[:n]]

    def mahasiswa_teraktif(self, n=3):
        c = Counter()
        for t in self.transaksi_service.semua():
            c[t.mahasiswa] += 1
        return [(m, jml) for m, jml in sorted(c.items(), key=lambda x: (-x[1], x[0].nim))[:n]]

    def jumlah_selesai(self):
        return sum(1 for t in self.transaksi_service.semua() if t.status == StatusTransaksi.SELESAI)

    def jumlah_aktif(self):
        return len(self.transaksi_service.aktif())

    def ringkasan(self):
        return {
            "alat_terpopuler": self.alat_terpopuler(),
            "mahasiswa_teraktif": self.mahasiswa_teraktif(),
            "transaksi_selesai": self.jumlah_selesai(),
            "transaksi_aktif": self.jumlah_aktif(),
        }
