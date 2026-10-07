class LogService:
    def __init__(self):
        self._logs = []

    def catat(self, pesan):
        self._logs.append(pesan)

    def semua(self):
        return list(self._logs)

    def tampilkan(self):
        if not self._logs:
            print("Belum ada aktivitas.")
            return

        print("\n=== LOG AKTIVITAS ===")
        for i, log in enumerate(self._logs, 1):
            print(f"{i}. {log}")