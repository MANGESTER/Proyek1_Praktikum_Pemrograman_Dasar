class MenuCLI:
    def __init__(
        self,
        mahasiswa_service,
        alat_service,
        transaksi_service,
        log_service=None,
        statistik_service=None
    ):
        self.mahasiswa_service = mahasiswa_service
        self.alat_service = alat_service
        self.transaksi_service = transaksi_service
        self.log_service = log_service
        self.statistik_service = statistik_service

    def tampilkan_menu(self):
        print("\n====================================")
        print(" SISTEM PEMINJAMAN ALAT LABORATORIUM")
        print("====================================")
        print("1. Tampilkan daftar mahasiswa")
        print("2. Tampilkan daftar alat")
        print("3. Pinjam alat")
        print("4. Kembalikan alat")
        print("5. Cari transaksi")
        print("6. Lihat riwayat transaksi")
        print("7. Lihat statistik")
        print("8. Lihat log aktivitas")
        print("9. Keluar")
        print("====================================")

    def jalankan(self):
        while True:
            self.tampilkan_menu()

            pilihan = input("Pilih menu: ").strip()

            if pilihan == "1":
                self.tampilkan_mahasiswa()

            elif pilihan == "2":
                self.tampilkan_alat()

            elif pilihan == "3":
                self.pinjam_alat()

            elif pilihan == "4":
                self.kembalikan_alat()

            elif pilihan == "5":
                self.cari_transaksi()

            elif pilihan == "6":
                self.lihat_riwayat()

            elif pilihan == "7":
                self.lihat_statistik()

            elif pilihan == "8":
                self.lihat_log()

            elif pilihan == "9":
                print("Program selesai.")
                break

            else:
                print("Pilihan menu tidak valid.")

    def tampilkan_mahasiswa(self):
        print("\n=== DAFTAR MAHASISWA ===")

        for mahasiswa in self.mahasiswa_service.semua():
            print(
                f"NIM: {mahasiswa.nim} | "
                f"Nama: {mahasiswa.nama}"
            )

    def tampilkan_alat(self):
        print("\n=== DAFTAR ALAT ===")

        for alat in self.alat_service.semua():
            print(
                f"Kode: {alat.kode} | "
                f"Nama: {alat.nama} | "
                f"Kategori: {alat.kategori} | "
                f"Kondisi: {alat.kondisi} | "
                f"Status: {alat.status}"
            )

    def pinjam_alat(self):
        print("\n=== PEMINJAMAN ALAT ===")

        nim = input("NIM mahasiswa: ").strip()
        kode = input("Kode alat (pisahkan koma): ").strip()
        lama = input("Lama peminjaman (hari): ").strip()

        try:
            daftar_kode = kode.split(",")
            lama_hari = int(lama)

            transaksi = self.transaksi_service.buat(
                nim,
                daftar_kode,
                lama_hari
            )

            print(f"Peminjaman berhasil. ID transaksi: {transaksi.id}")

        except Exception as e:
            print(f"Gagal melakukan peminjaman: {e}")

    def kembalikan_alat(self):
        print("\n=== PENGEMBALIAN ALAT ===")

        id_transaksi = input("ID transaksi: ").strip()
        kode = input("Kode alat: ").strip()
        kondisi = input(
            "Kondisi alat (Baik/Rusak Ringan/Rusak Berat): "
        ).strip()

        try:
            hasil = self.transaksi_service.kembalikan(
                id_transaksi,
                {kode: kondisi}
            )

            print("Pengembalian berhasil.")

            for detail in hasil:
                print(f"Alat {detail.kode_alat} berhasil dikembalikan.")

        except Exception as e:
            print(f"Gagal melakukan pengembalian: {e}")

    def cari_transaksi(self):
        print("\n=== CARI TRANSAKSI ===")

        keyword = input("Masukkan NIM/nama mahasiswa: ").strip()

        try:
            hasil = self.transaksi_service.cari_by_mahasiswa(keyword)

            if not hasil:
                print("Transaksi tidak ditemukan.")
                return

            for transaksi in hasil:
                print(transaksi)

        except Exception as e:
            print(f"Gagal mencari transaksi: {e}")

    def lihat_riwayat(self):
        print("\n=== RIWAYAT TRANSAKSI ===")

        nim = input("NIM mahasiswa: ").strip()

        try:
            hasil = self.transaksi_service.riwayat(nim)

            if not hasil:
                print("Belum ada riwayat transaksi.")
                return

            for transaksi in hasil:
                print(transaksi)

        except Exception as e:
            print(f"Gagal menampilkan riwayat: {e}")

    def lihat_statistik(self):
        print("\n=== STATISTIK ===")

        if self.statistik_service:
            self.statistik_service.tampilkan()
        else:
            print("StatistikService belum tersedia.")

    def lihat_log(self):
        print("\n=== LOG AKTIVITAS ===")

        if self.log_service:
            for log in self.log_service.semua():
                print(log)
        else:
            print("LogService belum tersedia.")
            la