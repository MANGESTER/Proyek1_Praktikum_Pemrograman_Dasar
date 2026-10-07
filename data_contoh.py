from models.alat import Alat, Kondisi_Baik, Kondisi_Rusak_Ringan

def buat_data_alat():
    return [
        Alat("A001", "Laptop Lenovo", "Komputer", Kondisi_Baik),
        Alat("A002", "Proyektor Epson", "Proyektor", Kondisi_Baik),
        Alat("A003", "Kabel HDMI", "Kabel", Kondisi_Baik),
        Alat("A004", "Mouse Logitech", "Periferal", Kondisi_Baik),
        Alat("A005", "Keyboard Logitech", "Periferal", Kondisi_Rusak_Ringan),
    ]
