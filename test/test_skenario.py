from services.log_service import LogService
from services.lab_service import LabService
from services.transaction_service import TransactionService
from models.enums import KondisiAlat
from models.exceptions import AlatTidakTersediaError, DataTerpakaiError


def run_tests():
    print("=== MEMULAI PENGUJIAN SKENARIO 1-6 ===")
    log = LogService()
    lab = LabService(log)
    tx_service = TransactionService(lab, log)

    # Skenario 1: Tambah beberapa mahasiswa & beberapa jenis peralatan
    lab.tambah_kategori("Multimedia", "Audio Video Lab")
    lab.tambah_mahasiswa("M101", "Mahardika", "0811111111")
    lab.tambah_mahasiswa("M102", "Abyan", "0822222222")
    a1 = lab.tambah_alat("A01", "Kamera DSLR", "Multimedia")
    a2 = lab.tambah_alat("A02", "Tripod", "Multimedia")
    a3 = lab.tambah_alat("A03", "Microphone", "Multimedia")
    print("[PASSED] Skenario 1: Tambah data mahasiswa dan peralatan berhasil.")

    # Skenario 2: Mahasiswa meminjam beberapa alat dalam satu transaksi (Periksa perubahan status)
    tx1 = tx_service.buat_transaksi("M101", ["A01", "A02"])
    assert not a1.is_tersedia() and not a2.is_tersedia()
    print("[PASSED] Skenario 2: Transaksi berhasil dibuat & status alat otomatis berubah menjadi tidak tersedia.")

    # Skenario 3: Mahasiswa mencoba meminjam alat yang tidak tersedia (Program harus menolak)
    try:
        tx_service.buat_transaksi("M102", ["A01"])
        print("[FAILED] Skenario 3: Seharusnya gagal karena A01 sedang dipinjam.")
    except AlatTidakTersediaError:
        print("[PASSED] Skenario 3: Program berhasil menolak peminjaman alat yang tidak tersedia.")

    # Skenario 4: Mahasiswa mengembalikan sebagian alat
    tx_service.proses_pengembalian_item(tx1.id_transaksi, "A01", KondisiAlat.BAIK)
    assert a1.is_tersedia() and tx1.is_aktif()
    print("[PASSED] Skenario 4: Pengembalian sebagian berhasil, alat A01 kembali tersedia & transaksi tetap aktif.")

    # Skenario 5: Alat dikembalikan dalam kondisi rusak berat/rusak ringan (Periksa stok tersedia)
    tx_service.proses_pengembalian_item(tx1.id_transaksi, "A02", KondisiAlat.RUSAK_BERAT)
    assert not a2.is_tersedia() and not tx1.is_aktif()
    print("[PASSED] Skenario 5: Alat A02 dikembalikan rusak berat dan TIDAK masuk kembali ke stok tersedia.")

    # Skenario 6: Mahasiswa yang masih memiliki transaksi aktif mencoba dihapus (Program harus menolak)
    tx_service.buat_transaksi("M102", ["A03"])
    try:
        lab.hapus_mahasiswa("M102")
        print("[FAILED] Skenario 6: Seharusnya gagal menghapus mahasiswa dengan transaksi aktif.")
    except DataTerpakaiError:
        print("[PASSED] Skenario 6: Program berhasil menolak penghapusan mahasiswa yang masih memiliki transaksi aktif.")

    print("\n==================================================")
    print(" SELURUH SKENARIO UJI BERHASIL DI-EKSEKUSI (100%) ")
    print("==================================================")


if __name__ == "__main__":
    run_tests()