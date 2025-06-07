import tkinter as tk
from tkinter import messagebox
import json
import os
import datetime

# === Data ===
file_json = "transaksi.json"
judul_bank = "BANK MINI SEKOLAH"
alamat_bank = "SMKN 1 PROBOLINGGO"

jenis_pembayaran = ["Uang Seragam", "Uang Gedung", "SPP", "LKS", "INDUSTRI"]
harga_pembayaran = [500000, 1000000, 150000, 300000, 100000]
metode_pembayaran = ["GoPay", "LinkAja", "Dana", "Transfer Bank", "Tunai"]

# === Fungsi untuk load dan save data ===
def load_transaksi():
    if os.path.exists(file_json):
        with open(file_json, "r") as f:
            return json.load(f)
    return []

def save_transaksi(data):
    with open(file_json, "w") as f:
        json.dump(data, f, indent=4)

# === Popup besar dengan struk transaksi ===
def popup_berhasil(transaksi):
    popup = tk.Toplevel()
    popup.title("Struk Transaksi")
    popup.geometry("500x400")

    teks = f"""
{judul_bank}
{alamat_bank}
--------------------------------------------
Tanggal     : {transaksi['tanggal']}
Nama Siswa  : {transaksi['nama_siswa']}
Kelas       : {transaksi['kelas_siswa']}
Jenis Bayar : {transaksi['jenis_pembayaran']}
Metode Bayar: {transaksi['metode_pembayaran']}
Jumlah Bayar: Rp {transaksi['jumlah']:,}
Uang Dibayar: Rp {transaksi['uang_bayar']:,}
Kembalian   : Rp {transaksi['kembalian']:,}
--------------------------------------------
Terima kasih telah melakukan transaksi!
"""

    label = tk.Label(popup, text=teks, font=("Arial", 12), justify="left", padx=20, pady=20)
    label.pack()

    tombol_ok = tk.Button(popup, text="Tutup", font=("Arial", 12, "bold"), command=popup.destroy)
    tombol_ok.pack(pady=10)

    popup.transient(root)
    popup.grab_set()

# === Simpan transaksi utama ===
def simpan_transaksi():
    nama = entry_nama.get()
    kelas = entry_kelas.get()
    jenis = jenis_var.get()
    metode = metode_var.get()

    if not nama or not kelas:
        messagebox.showerror("Error", "Nama dan Kelas harus diisi!")
        return

    index = jenis_pembayaran.index(jenis)
    harga = harga_pembayaran[index]
    tanggal = datetime.datetime.now().strftime("%d %B %Y %H:%M:%S")

    try:
        dibayar = int(entry_bayar.get())
    except ValueError:
        messagebox.showerror("Error", "Jumlah uang yang dibayarkan harus angka!")
        return

    if dibayar < harga:
        messagebox.showerror("Error", "Uang dibayar kurang dari harga!")
        return

    kembalian = dibayar - harga

    transaksi = load_transaksi()
    transaksi_baru = {
        "tanggal": tanggal,
        "nama_siswa": nama,
        "kelas_siswa": kelas,
        "jenis_pembayaran": jenis,
        "jumlah": harga,
        "metode_pembayaran": metode,
        "uang_bayar": dibayar,
        "kembalian": kembalian
    }
    transaksi.append(transaksi_baru)
    save_transaksi(transaksi)

    popup_berhasil(transaksi_baru)

    entry_nama.delete(0, tk.END)
    entry_kelas.delete(0, tk.END)
    entry_bayar.delete(0, tk.END)

# === GUI Utama ===
root = tk.Tk()
root.title("Aplikasi Bank Mini Sekolah")

tk.Label(root, text=judul_bank, font=("Arial", 16, "bold")).pack()
tk.Label(root, text=alamat_bank, font=("Arial", 11)).pack(pady=(0, 10))

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Nama Siswa", font=("Arial", 11)).grid(row=0, column=0, sticky="w")
entry_nama = tk.Entry(frame, font=("Arial", 11))
entry_nama.grid(row=0, column=1)

tk.Label(frame, text="Kelas Siswa", font=("Arial", 11)).grid(row=1, column=0, sticky="w")
entry_kelas = tk.Entry(frame, font=("Arial", 11))
entry_kelas.grid(row=1, column=1)

tk.Label(frame, text="Jenis Pembayaran", font=("Arial", 11)).grid(row=2, column=0, sticky="w")
jenis_var = tk.StringVar()
jenis_var.set(jenis_pembayaran[0])
tk.OptionMenu(frame, jenis_var, *jenis_pembayaran).grid(row=2, column=1)

tk.Label(frame, text="Metode Pembayaran", font=("Arial", 11)).grid(row=3, column=0, sticky="w")
metode_var = tk.StringVar()
metode_var.set(metode_pembayaran[0])
tk.OptionMenu(frame, metode_var, *metode_pembayaran).grid(row=3, column=1)

tk.Label(frame, text="Jumlah Dibayar (Rp)", font=("Arial", 11)).grid(row=4, column=0, sticky="w")
entry_bayar = tk.Entry(frame, font=("Arial", 11))
entry_bayar.grid(row=4, column=1)

tk.Button(root, text="Simpan Transaksi", font=("Arial", 12, "bold"), command=simpan_transaksi).pack(pady=15)

root.mainloop()