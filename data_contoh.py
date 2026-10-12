"""Data contoh untuk demo (menu 16)."""
from models.exceptions import DataDuplikat


def muat(mahasiswa_service, alat_service):
    mahasiswa = [("M001", "Ani Lestari", "081234567890"),
                 ("M002", "Budi Santoso", "082345678901"),
                 ("M003", "Citra Dewi", "083456789012")]
    alat = [("K001", "Laptop Dell", "Perangkat Komputasi"),
            ("K002", "Raspberry Pi 4", "Perangkat Komputasi"),
            ("J001", "Router Cisco", "Perangkat Jaringan"),
            ("J002", "Kabel LAN 5m", "Perangkat Jaringan"),
            ("M001", "Kamera Digital", "Perangkat Multimedia"),
            ("M002", "Tripod", "Perangkat Multimedia")]
    n = 0
    for data in mahasiswa:
        try:
            mahasiswa_service.tambah(*data); n += 1
        except DataDuplikat:
            pass
    for data in alat:
        try:
            alat_service.tambah(*data); n += 1
        except DataDuplikat:
            pass
    return n
