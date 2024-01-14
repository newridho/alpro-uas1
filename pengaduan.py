import tkinter as tk
import ttkbootstrap as ttk
from datetime import datetime
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
        # self.create_table()


        # Label untuk judul
        label_judul = tk.Label(root, text="Pengaduan Rakyat", font=("Helvetica", 20, "bold"))
        label_judul.pack(pady=(15))

        # Button untuk ajukan pengaduan
        btn_ajukan_pengaduan = ttk.Button(root, text="Ajukan Pengaduan", command=self.ajukan_pengaduan, bootstyle="success.Outline", width="40")
        btn_ajukan_pengaduan.pack(pady=(20,10))

        # Button untuk tampilkan pengaduan
        btn_tampilkan_pengaduan = ttk.Button(root, text="Tampilkan Pengaduan", command=self.tampilkan_pengaduan, bootstyle="primary.Outline", width="40")
        btn_tampilkan_pengaduan.pack(pady=(5, 20))

        # Button untuk keluar
        btn_keluar = ttk.Button(root, text="Keluar", command=self.keluar, bootstyle="danger.Solid", width="15")
        btn_keluar.pack(padx=1)

    # def create_table(self):
    #     # Membuat tabel 'pengaduan' jika belum ada
    #     cursor = self.db.cursor()
    #     cursor.execute("""
    #         CREATE TABLE IF NOT EXISTS pengaduan (
    #             id INT AUTO_INCREMENT PRIMARY KEY,
    #             isi TEXT
    #         )
    #     """)
    #     self.db.commit()

    def ajukan_pengaduan(self):
        # Fungsi untuk ajukan pengaduan
        judul_laporanB = simpledialog.askstring("Ajukan Pengaduan", "Masukkan Judul Pengaduan :")
        tgl_kejadian = datetime.now()
        lok_kejadianB = simpledialog.askstring("Ajukan Pengaduan", "Masukkan Lokasi Kejadian :")
        instansiB = simpledialog.askstring("Ajukan Pengaduan", "Masukkan Instansi Tujuan : ")
        isi_laporanB = simpledialog.askstring("Ajukan Pengaduan", "Masukkan Isi Laporan : ")
        # if judul_laporanB and lok_kejadianB and instansiB:
        while True:
            self.simpan_pengaduan(judul_laporanB,tgl_kejadian,lok_kejadianB,instansiB,isi_laporanB)
            messagebox.showinfo("Sukses", "Pengaduan berhasil diajukan.")
            break

        # return judul_laporanB,tgl_kejadian,lok_kejadianB,instansiB,isi_laporanB

    def simpan_pengaduan(self,judul_laporanB,tgl_kejadian,lok_kejadianB,instansiB,isi_laporanB):
        # Fungsi untuk menyimpan pengaduan ke dalam database
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO pengaduan (judul_laporan,tgl_kejadian,lokasi_kejadian,instansi_tujuan,isi_laporan) VALUES (%s,%s,%s,%s,%s)", (judul_laporanB,tgl_kejadian,lok_kejadianB,instansiB,isi_laporanB))
        self.db.commit()

    def tampilkan_pengaduan(self):
        # Fungsi untuk tampilkan pengaduan
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM pengaduan")
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

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_pengaduan"
    )

    root = ttk.Window(themename="cyborg")
    root.title("Pengaduan Rakyat")
    root.iconbitmap('images/uty.ico')
    root.geometry('500x350')

    app = PengaduanApp(root, db)
    root.mainloop()
    
    db.close()
