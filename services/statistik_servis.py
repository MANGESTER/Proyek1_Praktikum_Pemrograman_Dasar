from collections import Counter


class StatistikService:
    def __init__(self, transaction_service, lab_service):
        self.tx_service = transaction_service
        self.lab_service = lab_service

    def alat_paling_sering_dipinjam(self):
        """
        Menghitung frekuensi peminjaman setiap alat.
        Mengembalikan list tuple [(nama_alat, frekuensi), ...]
        """
        counter = Counter()
        for tx in self.tx_service.transaksi_dict.values():
            for item in tx.daftar_item:
                counter[item.alat.nama] += 1
        return counter.most_common()

    def mahasiswa_paling_aktif(self):
        """
        Menghitung frekuensi transaksi berdasarkan mahasiswa.
        Mengembalikan list tuple [(nama_mhs (NIM), total_tx), ...]
        """
        counter = Counter()
        for tx in self.tx_service.transaksi_dict.values():
            label = f"{tx.mahasiswa.nama} ({tx.mahasiswa.nim})"
            counter[label] += 1
        return counter.most_common()

    def ringkasan_transaksi(self):
        """
        Mengembalikan ringkasan statistik transaksi: total, selesai, dan aktif.
        """
        total = len(self.tx_service.transaksi_dict)
        selesai = sum(1 for tx in self.tx_service.transaksi_dict.values() if not tx.is_aktif())
        aktif = total - selesai
        return {
            "total": total,
            "selesai": selesai,
            "aktif": aktif
        }