"""Titik masuk aplikasi Sistem Peminjaman Peralatan Laboratorium."""
from services.alat_service import AlatService
from services.log_service import LogService
from services.mahasiswa_service import MahasiswaService
from services.statistik_service import StatistikService
from services.transaksi_service import TransaksiService
from ui.menu import MenuCLI


def main():
    log = LogService()
    mahasiswa_service = MahasiswaService(log)
    alat_service = AlatService(log)
    transaksi_service = TransaksiService(mahasiswa_service, alat_service, log)
    statistik_service = StatistikService(transaksi_service)
    MenuCLI(mahasiswa_service, alat_service, transaksi_service, log, statistik_service).jalankan()


if __name__ == "__main__":
    main()
