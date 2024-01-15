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
        self.cursor = self.db.cursor()

        # self.tampilkan_pengaduan(db)

        # Label untuk judul
        mainFrame = ttk.Frame(root, padding=15)
        mainFrame.pack(fill = BOTH, expand = True)

        label_judul = ttk.Label(mainFrame, text="Pengaduan Rakyat", font=("Helvetica", 20, "bold"))
        label_desc = ttk.Label(mainFrame, text="Daerah Yogyakarta", font=("Helvetica", 10, "bold"), bootstyle="danger")
        label_judul.pack(pady=(1))
        label_desc.pack(pady=(1))
        # label_desc.pack(after=())

        # Button untuk ajukan pengaduan
        btn_ajukan_pengaduan = ttk.Button(mainFrame, text="Ajukan Pengaduan", command=self.ajukan_pengaduan, bootstyle="success.Outline", width="40")
        btn_ajukan_pengaduan.pack(pady=(20,10))

        # Button untuk tampilkan pengaduan
        btn_tampilkan_pengaduan = ttk.Button(mainFrame, text="Tampilkan Pengaduan", command=self.tampilkan_pengaduan, bootstyle="primary.Outline", width="40")
        btn_tampilkan_pengaduan.pack(pady=(5, 20))

        # Button untuk keluar
        btn_keluar = ttk.Button(mainFrame, text="Keluar", command=self.keluar, bootstyle="danger.Solid", width="15")
        btn_keluar.pack(pady=5)

    def ajukan_pengaduan(self):
        # Fungsi untuk ajukan pengaduan
        judul_laporanB = simpledialog.askstring("Ajukan Pengaduan", "Masukkan Judul Pengaduan :")
        tgl_kejadian = datetime.now()
        lok_kejadianB = simpledialog.askstring("Ajukan Pengaduan", "Masukkan Lokasi Kejadian :")
        instansiB = simpledialog.askstring("Ajukan Pengaduan", "Masukkan Instansi Tujuan : ")
        isi_laporanB = simpledialog.askstring("Ajukan Pengaduan", "Masukkan Isi Laporan : ")
        # if judul_laporanB and lok_kejadianB and instansiB:
        if judul_laporanB is not None :
            self.simpan_pengaduan(judul_laporanB,tgl_kejadian,lok_kejadianB,instansiB,isi_laporanB)
            messagebox.showinfo("Sukses", "Pengaduan berhasil diajukan.")
        else :
            self.root.destroy()

        # return judul_laporanB,tgl_kejadian,lok_kejadianB,instansiB,isi_laporanB

    def simpan_pengaduan(self,judul_laporanB,tgl_kejadian,lok_kejadianB,instansiB,isi_laporanB):
        # Fungsi untuk menyimpan pengaduan ke dalam database
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO pengaduan (judul_laporan,tgl_kejadian,lokasi_kejadian,instansi_tujuan,isi_laporan) VALUES (%s,%s,%s,%s,%s)", (judul_laporanB,tgl_kejadian,lok_kejadianB,instansiB,isi_laporanB))
        self.db.commit()

    def tampilkan_pengaduan(self, db):

        self.tree = ttk.Treeview(root, columns=('id', 'judul_laporan', 'isi_laporan', 'tgl_kejadian', 'lokasi_kejadian', 'instansi_tujuan'))
        self.tree.heading('#0', text='ID')
        self.tree.heading('#1', text='Judul Laporan')
        self.tree.heading('#3', text='Tanggal Kejadian')
        self.tree.heading('#4', text='Lokasi Kejadian')
        self.tree.heading('#5', text='Instansi Tujuan')
        self.tree.heading('#6', text='Isi Laporan')
        self.tree.pack()

        tabelFrame= ttk.Frame(root, padding=15, bootstyle="primary")
        tabelFrame.pack(fill = BOTH, expand = True)

        # Buat Treeview untuk menampilkan data
        

        for i in self.tree.get_children():
            self.tree.delete(i)

        # Ambil data dari database
        self.cursor.execute("SELECT * FROM pengaduan")
        rows = self.cursor.fetchall()

        # Tampilkan data di Treeview
        for row in rows:
            self.tree.insert('', 'end', values=row)

        if not rows:
            messagebox.showinfo("Info", "Belum ada pengaduan.")
        else:
            tampilkan_window = tk.Toplevel(self.root)
            tampilkan_window.title("Tampilkan Pengaduan")

            listbox_pengaduan = tk.Listbox(tampilkan_window)
            listbox_pengaduan.pack()

            for i, pengaduan in enumerate(rows, start=1):
                listbox_pengaduan.insert(tk.END, f"{i}. {pengaduan[1]} \t {pengaduan[2]} \t {pengaduan[3]} \t {pengaduan[4]} \n {pengaduan[5]}")

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
    root.iconbitmap(default='images/uty.ico')
    root.geometry('500x350')

    app = PengaduanApp(root, db)
    root.mainloop()
    
    db.close()
