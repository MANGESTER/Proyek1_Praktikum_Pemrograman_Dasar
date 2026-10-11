from services.alat_service import AlatService
from services.log_service import LogService
from services.mahasiswa_service import MahasiswaService
from services.statistik_service import StatistikService
from services.transaksi_service import TransaksiService
from ui.menu import MenuCLI


def main():
    log = LogService()
    mahasiswa = MahasiswaService(log)
    alat = AlatService(log)
    transaksi = TransaksiService(mahasiswa, alat, log)
    statistik = StatistikService(transaksi)
    MenuCLI(mahasiswa, alat, transaksi, statistik, log).jalan()


if __name__ == "__main__":
    main()
 