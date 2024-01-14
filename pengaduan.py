import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox, simpledialog
from ttkbootstrap.constants import *
from ttkbootstrap import Style
import mysql.connector

class PengaduanApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Aplikasi Pengaduan")

        # Membuat tabel pengaduan jika belum ada
        self.create_table()

        # Label untuk judul
        label_judul = tk.Label(root, text="Pengaduan Rakyat", font=("Helvetica", 16, "bold"))
        label_judul.pack(pady=20)

        # Button untuk ajukan pengaduan
        btn_ajukan_pengaduan = ttk.Button(root, text="Ajukan Pengaduan", command=self.ajukan_pengaduan, bootstyle="info.Outline")
        btn_ajukan_pengaduan.pack(pady=20)

        # Button untuk tampilkan pengaduan
        btn_tampilkan_pengaduan = tk.Button(root, text="Tampilkan Pengaduan", command=self.tampilkan_pengaduan)
        btn_tampilkan_pengaduan.pack(pady=20)

        # Button untuk keluar
        btn_keluar = tk.Button(root, text="Keluar", command=self.keluar)
        btn_keluar.pack(pady=20)

    def create_table(self):
        # Membuat tabel 'pengaduan' jika belum ada
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pengaduan (
                id INT AUTO_INCREMENT PRIMARY KEY,
                isi TEXT
            )
        """)
        self.db.commit()

    def ajukan_pengaduan(self):
        # Fungsi untuk ajukan pengaduan
        pengaduan_baru = simpledialog.askstring("Ajukan Pengaduan", "Masukkan pengaduan:")
        if pengaduan_baru:
            self.simpan_pengaduan(pengaduan_baru)
            messagebox.showinfo("Sukses", "Pengaduan berhasil diajukan.")

    def simpan_pengaduan(self, isi_pengaduan):
        # Fungsi untuk menyimpan pengaduan ke dalam database
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO pengaduan (isi) VALUES (%s)", (isi_pengaduan,))
        self.db.commit()

    def tampilkan_pengaduan(self):
        # Fungsi untuk tampilkan pengaduan
        cursor = self.db.cursor()
        cursor.execute("SELECT isi FROM pengaduan")
        result = cursor.fetchall()

        if not result:
            messagebox.showinfo("Info", "Belum ada pengaduan.")
        else:
            tampilkan_window = tk.Toplevel(self.root)
            tampilkan_window.title("Tampilkan Pengaduan")

            listbox_pengaduan = tk.Listbox(tampilkan_window)
            listbox_pengaduan.pack()

            for i, pengaduan in enumerate(result, start=1):
                listbox_pengaduan.insert(tk.END, f"{i}. {pengaduan[0]}")

    def keluar(self):
        # Fungsi untuk keluar
        confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin keluar?")
        if confirm:
            self.root.destroy()

if __name__ == "__main__":
    # Ganti nilai host, user, password, dan database sesuai dengan konfigurasi MySQL Anda
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="pengaduan"
    )

    root = ttk.Window(themename="cyborg")
    app = PengaduanApp(root, db)
    root.mainloop()

    # Tutup koneksi database setelah aplikasi ditutup
    db.close()
