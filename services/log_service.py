"""Tantangan D: log aktivitas (disimpan dalam list of dict)."""
from datetime import datetime


class LogService:
    def __init__(self):
        self.entri = []  # list of {"waktu": datetime, "pesan": str}

    def catat(self, pesan, waktu=None):
        self.entri.append({"waktu": waktu or datetime.now(), "pesan": pesan})

    def semua(self):
        return [f"[{e['waktu'].strftime('%Y-%m-%d %H:%M')}] {e['pesan']}" for e in self.entri]

    def tampilkan(self):
        baris = self.semua()
        print("\n".join(baris) if baris else "(Belum ada aktivitas)")