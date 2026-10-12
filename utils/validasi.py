"""Fungsi validasi input. Melempar ValueError bila input tidak valid."""
import re
from datetime import datetime, date

def wajib_isi(nilai, label="Data"):
    teks = str(nilai).strip()
    if not teks:
        raise ValueError(f"{label} tidak boleh kosong.")
    return teks

def validasi_nim(nim):
    nim = wajib_isi(nim, "NIM")
    if not nim.isalnum():
        raise ValueError("NIM hanya boleh berisi huruf dan angka.")
    return nim.upper()

def validasi_kode(kode):
    kode = wajib_isi(kode, "Kode alat")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", kode):
        raise ValueError("Kode alat hanya boleh huruf, angka, '-' atau '_'.")
    return kode.upper()

def validasi_no_hp(no_hp):
    no_hp = wajib_isi(no_hp, "Nomor HP")
    if not re.fullmatch(r"\+?\d{8,15}", no_hp):
        raise ValueError("Nomor HP harus 8-15 digit angka.")
    return no_hp

def parse_angka(teks, label="Angka"):
    try:
        return int(str(teks).strip())
    except ValueError:
        raise ValueError(f"{label} harus berupa bilangan bulat.")

def parse_tanggal(teks, label="Tanggal"):
    """Format tanggal: YYYY-MM-DD."""
    if isinstance(teks, date):
        return teks
    try:
        return datetime.strptime(str(teks).strip(), "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"{label} harus berformat YYYY-MM-DD.")
