import tkinter as tk
import ttkbootstrap as ttk
from datetime import datetime
from tkinter import messagebox, simpledialog
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
# from ttkbootstrap import Style
import mysql.connector

class PengaduanApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.colors = colors
        self.root.title("Aplikasi Pengaduan")
        self.cursor = self.db.cursor()

        mainFrame = ttk.Frame(root, padding=15)
        mainFrame.pack(fill=tk.BOTH, expand=True)

        label_judul = ttk.Label(mainFrame, text="Pengaduan Rakyat", font=("Helvetica", 20, "bold"))
        label_desc = ttk.Label(mainFrame, text="Daerah Yogyakarta", font=("Helvetica", 10, "bold"), bootstyle="danger")
        label_judul.pack(pady=1)
        label_desc.pack(pady=1)

        btn_ajukan_pengaduan = ttk.Button(mainFrame, text="Ajukan Pengaduan", command=self.ajukan_pengaduan, bootstyle="success.Outline", width="40")
        btn_ajukan_pengaduan.pack(pady=(20, 10))

        btn_tampilkan_pengaduan = ttk.Button(mainFrame, text="Tampilkan Pengaduan", command=self.tampilkan_pengaduan, bootstyle="primary.Outline", width="40")
        btn_tampilkan_pengaduan.pack(pady=(5, 20))

        btn_keluar = ttk.Button(mainFrame, text="Keluar", command=self.keluar, bootstyle="danger.Solid", width="15")
        btn_keluar.pack(pady=5)

    def ajukan_pengaduan(self):
        judul_laporanB = simpledialog.askstring("Ajukan Pengaduan", "Masukkan Judul Pengaduan :")
        tgl_kejadian = datetime.now()
        lok_kejadianB = simpledialog.askstring("Ajukan Pengaduan", "Masukkan Lokasi Kejadian :")
        instansiB = simpledialog.askstring("Ajukan Pengaduan", "Masukkan Instansi Tujuan : ")
        isi_laporanB = simpledialog.askstring("Ajukan Pengaduan", "Masukkan Isi Laporan : ")
        
        if judul_laporanB and lok_kejadianB and instansiB and isi_laporanB:
            self.simpan_pengaduan(judul_laporanB, tgl_kejadian, lok_kejadianB, instansiB, isi_laporanB)
            self.tampilkan_info_pengaduan(judul_laporanB, tgl_kejadian, lok_kejadianB, instansiB, isi_laporanB)

    def simpan_pengaduan(self, judul_laporanB, tgl_kejadian, lok_kejadianB, instansiB, isi_laporanB):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO pengaduan (judul_laporan, tgl_kejadian, lokasi_kejadian, instansi_tujuan, isi_laporan) VALUES (%s, %s, %s, %s, %s)",
                       (judul_laporanB, tgl_kejadian, lok_kejadianB, instansiB, isi_laporanB))
        self.db.commit()

    def tampilkan_info_pengaduan(self, judul, tanggal, lokasi, instansi, isi):
        info_window = tk.Toplevel(self.root)
        info_window.title("Info Pengaduan")

        info_text = f"Judul: {judul}\nTanggal Kejadian: {tanggal}\nLokasi Kejadian: {lokasi}\nInstansi Tujuan: {instansi}\nIsi Laporan: {isi}"

        info_label = ttk.Label(info_window, text=info_text, font=("Helvetica", 12))
        info_label.pack(padx=20, pady=20)

    def tampilkan_pengaduan(self):
        # tampilkan_window = tk.Tk()
        tampilkan_window = tk.Toplevel(self.root)
        tampilkan_window.title("Tampilkan Pengaduan")

        # self.tree = ttk.Treeview(tampilkan_window, bootstyle="warning.Treeview")
        columns=('id', 'judul_laporan', 'tgl_kejadian', 'lokasi_kejadian', 'instansi_tujuan', 'isi_laporan')
        coldata = [
            {"text": "Laporan ke-", "stretch":False},
            {"text": "Judul Laporan", "stretch":False},
            {"text": "Isi Laporan", "stretch":False},
            {"text": "Tanggal Kejadian", "stretch":False},
            {"text": "Lokasi Kejadian", "stretch":False},
            {"text": "Instansi Tujuan", "stretch":False},
        ]

        # self.tree.heading('#0', text='Laporan ke-')
        # self.tree.heading('#1', text='Judul Laporan')
        # self.tree.heading('#2', text='Isi Laporan')
        # self.tree.heading('#3', text='Tanggal Kejadian')
        # self.tree.heading('#4', text='Lokasi Kejadian')
        # self.tree.heading('#5', text='Instansi Tujuan')

        self.cursor.execute("SELECT * FROM pengaduan")
        rows = self.cursor.fetchall()

        
        table = Tableview(
            master=tampilkan_window,
            coldata=coldata,
            rowdata=rows,
            paginated=True,
            autofit=False,
            searchable=True,
            bootstyle=PRIMARY,
            stripecolor=(colors.dark, 'green', NONE),
        )

        table.pack(fill=ttk.BOTH, expand=YES, padx=10, pady=10)
            
        for row in rows:
            table.insert_row('end')
            table.load_table_data()
            roows=table.tablerows
            # print(row[1].values)

        if not rows:
            messagebox.showinfo("Info", "Belum ada pengaduan.")

    def keluar(self):
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

    colors = root.style.colors
    app = PengaduanApp(root, db)
    root.mainloop()

    db.close()
