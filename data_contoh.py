def muat_data_contoh(mhs, alat):
    for nim, nama, hp in [("M001", "Dika", "081234567890"), ("M002", "Abyan", "081234567891"),
                          ("M003", "Ayun", "081234567892"), ("M004", "Adibah", "081234567893")]:
        mhs.tambah(nim, nama, hp)
    for kode, nama, kat in [("A001", "Laptop", "perangkat komputasi"), ("A002", "Raspberry Pi", "perangkat komputasi"),
                            ("A003", "Router", "perangkat jaringan"), ("A004", "Kabel LAN", "perangkat jaringan"),
                            ("A005", "Kamera Digital", "perangkat multimedia"), ("A006", "Tripod", "perangkat multimedia"),
                            ("A007", "Multimeter", "perangkat elektronik"), ("A008", "Multimeter", "perangkat elektronik")]:
        alat.tambah(kode, nama, kat)