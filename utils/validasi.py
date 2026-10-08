import re


class ValidasiUtil:
    @staticmethod
    def is_valid_nim(nim: str) -> bool:
        """Validasi NIM (alfanumerik, panjang 3-15 karakter)."""
        if not nim:
            return False
        return bool(re.match(r"^[A-Za-z0-9]{3,15}$", nim.strip()))

    @staticmethod
    def is_valid_hp(hp: str) -> bool:
        """Validasi nomor HP (hanya angka/tanda +, panjang 10-15 digit)."""
        if not hp:
            return False
        return bool(re.match(r"^\+?[0-9]{10,15}$", hp.strip()))

    @staticmethod
    def is_not_empty(text: str) -> bool:
        """Validasi teks tidak boleh kosong atau sekadar spasi."""
        return bool(text and text.strip())