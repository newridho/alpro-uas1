import tkinter as tk
import ttkbootstrap as ttk
from datetime import datetime
from tkinter import messagebox, simpledialog
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from tkinter import Label, Entry, Button, Toplevel
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
# from ttkbootstrap import Style
import mysql.connector

class PengaduanApp:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        self.colors = colors
        self.master.title("Aplikasi Pengaduan")
        self.cursor = self.db.cursor()

        mainFrame = ttk.Frame(master, padding=15)
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
        class DataEntryForm(ttk.Frame):

            def __init__(self, master):
                super().__init__(master, padding=(20, 10))
                self.pack(fill=BOTH, expand=YES)

                # form variables
                self.judul_laporanB = ttk.StringVar(value="")
                self.tgl_kejadian = ttk.StringVar(value="")
                self.lok_kejadianB = ttk.StringVar(value="")
                self.instansiB = ttk.StringVar(value="")
                self.isi_laporanB = ttk.StringVar(value="")

                # form header
                hdr_txt = "Masukkan Aduan Anda" 
                hdr = ttk.Label(master=self, text=hdr_txt, width=50)
                hdr.pack(fill=X, pady=10)

                # form entries
                self.create_form_entry("Judul Laporan", self.judul_laporanB)
                self.create_form_entry("Tanggal Kejadian", self.tgl_kejadian)
                self.create_form_entry("Lokasi Kejadian", self.lok_kejadianB)
                self.create_form_entry("Instansi Tujuan", self.instansiB)
                self.create_form_entry("Isi Laporan", self.isi_laporanB)
                self.create_buttonbox()

            def create_form_entry(self, label, variable):
                """Create a single form entry"""
                container = ttk.Frame(self)
                container.pack(fill=X, expand=YES, pady=5)

                lbl = ttk.Label(master=container, text=label.title(), width=10)
                lbl.pack(side=LEFT, padx=5)

                ent = ttk.Entry(master=container, textvariable=variable)
                ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

            def create_buttonbox(self):
                """Create the application buttonbox"""
                container = ttk.Frame(self)
                container.pack(fill=X, expand=YES, pady=(15, 10))

                sub_btn = ttk.Button(
                    master=container,
                    text="Submit",
                    command=self.on_submit,
                    bootstyle=SUCCESS,
                    width=6,
                )
                sub_btn.pack(side=RIGHT, padx=5)
                sub_btn.focus_set()

                cnl_btn = ttk.Button(
                    master=container,
                    text="Cancel",
                    command=self.on_cancel,
                    bootstyle=DANGER,
                    width=6,
                )
                cnl_btn.pack(side=RIGHT, padx=5)

            def on_submit(self):
                """Print the contents to console and return the values."""
                print("Judul Laporan:", self.judul_laporanB.get())
                print("Tanggal Kejadian:", self.tgl_kejadian.get())
                print("Lokasi Kejadian:", self.lok_kejadianB.get())
                print("Instansi Tujuan:", self.instansiB.get())
                print("Isi Laporan:", self.isi_laporanB.get())
                return self.judul_laporanB.get(), self.tgl_kejadian.get(), self.lok_kejadianB.get(), self.instansiB.get(), self.isi_laporanB.get()

            def on_cancel(self):
                """Cancel and close the application."""
                self.master.destroy()


        if __name__ == "__main__":

            app = ttk.Window("Data Entry", "cyborg", resizable=(False, False))
            DataEntryForm(app)
            app.mainloop()

    def simpan_pengaduan(self, judul_laporanB, tgl_kejadian, lok_kejadianB, instansiB, isi_laporanB):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO pengaduan (judul_laporan, tgl_kejadian, lokasi_kejadian, instansi_tujuan, isi_laporan) VALUES (%s, %s, %s, %s, %s)",
                       (judul_laporanB, tgl_kejadian, lok_kejadianB, instansiB, isi_laporanB))
        self.db.commit()

    def tampilkan_info_pengaduan(self, judul, tanggal, lokasi, instansi, isi):
        info_window = tk.Toplevel(self.master)
        info_window.title("Info Pengaduan")

        info_text = f"Judul: {judul}\nTanggal Kejadian: {tanggal}\nLokasi Kejadian: {lokasi}\nInstansi Tujuan: {instansi}\nIsi Laporan: {isi}"

        info_label = ttk.Label(info_window, text=info_text, font=("Helvetica", 12))
        info_label.pack(padx=20, pady=20)

    def tampilkan_pengaduan(self):
        # tampilkan_window = tk.Tk()
        tampilkan_window = tk.Toplevel(self.master)
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
            self.master.destroy()

if __name__ == "__main__":
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_pengaduan"
    )

    master = ttk.Window(themename="cyborg")
    master.title("Pengaduan Rakyat")
    master.iconbitmap(default='images/uty.ico')
    master.geometry('500x350')

    colors = master.style.colors
    app = PengaduanApp(master, db)
    master.mainloop()

    db.close()
