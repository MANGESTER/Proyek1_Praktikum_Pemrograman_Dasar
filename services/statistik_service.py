class StatistikService:
    def __init__(self, mahasiswa_service, alat_service, transaksi_service):
        self._mhs = mahasiswa_service
        self._alat = alat_service
        self._transaksi = transaksi_service

    def jumlah_transaksi(self):
        return len(self._transaksi.semua())

    def jumlah_transaksi_aktif(self):
        return len(self._transaksi.aktif())

    def jumlah_transaksi_selesai(self):
        return len(self._transaksi.selesai())

    def tampilkan(self):
        print("\n=== STATISTIK SISTEM ===")
        print(f"Jumlah transaksi : {self.jumlah_transaksi()}")
        print(f"Transaksi aktif  : {self.jumlah_transaksi_aktif()}")
        print(f"Transaksi selesai: {self.jumlah_transaksi_selesai()}")
    