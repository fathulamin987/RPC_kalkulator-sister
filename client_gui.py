import tkinter as tk
import xmlrpc.client


# koneksi ke server
server = xmlrpc.client.ServerProxy("http://localhost:8000")


# variabel
angka_pertama = None
operasi = None
reset_display = False


# format angka
def format_angka(angka):
    if isinstance(angka, str):
        return angka

    if isinstance(angka, float) and angka.is_integer():
        angka = int(angka)

    if isinstance(angka, int):
        return f"{angka:,}".replace(",", ".")

    teks = str(angka)

    if "." in teks:
        depan, belakang = teks.split(".")
        depan = f"{int(depan):,}".replace(",", ".")
        return depan + "," + belakang

    return teks


# ambil angka
def ambil_angka():
    teks = display.get()
    teks = teks.replace(".", "")
    teks = teks.replace(",", ".")
    return float(teks)


# input angka
def tekan_angka(angka):
    global reset_display

    if reset_display:
        display.delete(0, tk.END)
        reset_display = False

    if display.get() == "0":
        display.delete(0, tk.END)

    display.insert(tk.END, angka)


# input koma
def tekan_koma():
    global reset_display

    if reset_display:
        display.delete(0, tk.END)
        display.insert(0, "0")
        reset_display = False

    if "," not in display.get():
        display.insert(tk.END, ",")


# pilih operasi
def pilih_operasi(op):
    global angka_pertama
    global operasi
    global reset_display

    try:
        angka_pertama = ambil_angka()
        operasi = op

        label_ekspresi.config(
            text=format_angka(angka_pertama) + " " + op
        )

        display.delete(0, tk.END)
        reset_display = False

    except ValueError:
        display.delete(0, tk.END)
        display.insert(0, "Error")


# hitung
def hitung():
    global angka_pertama
    global operasi
    global reset_display

    if angka_pertama is None or operasi is None:
        return

    try:
        angka_kedua = ambil_angka()

        # panggil fungsi RPC
        if operasi == "+":
            hasil = server.tambah(angka_pertama, angka_kedua)

        elif operasi == "-":
            hasil = server.kurang(angka_pertama, angka_kedua)

        elif operasi == "×":
            hasil = server.kali(angka_pertama, angka_kedua)

        elif operasi == "÷":
            hasil = server.bagi(angka_pertama, angka_kedua)

        # tampilkan ekspresi
        label_ekspresi.config(
            text=format_angka(angka_pertama)
            + " "
            + operasi
            + " "
            + format_angka(angka_kedua)
        )

        # tampilkan hasil
        display.delete(0, tk.END)
        display.insert(0, format_angka(hasil))

        angka_pertama = None
        operasi = None
        reset_display = True

    except Exception:
        display.delete(0, tk.END)
        display.insert(0, "Error")


# hapus semua
def hapus_semua():
    global angka_pertama
    global operasi
    global reset_display

    display.delete(0, tk.END)
    display.insert(0, "0")

    label_ekspresi.config(text="")

    angka_pertama = None
    operasi = None
    reset_display = False


# hapus satu
def hapus_satu():
    isi = display.get()

    if len(isi) > 1:
        display.delete(len(isi) - 1, tk.END)
    else:
        display.delete(0, tk.END)
        display.insert(0, "0")


# keyboard
def keyboard(event):
    tombol = event.keysym
    karakter = event.char

    if karakter in "0123456789":
        tekan_angka(karakter)

    elif karakter == "+":
        pilih_operasi("+")

    elif karakter == "-":
        pilih_operasi("-")

    elif karakter == "*":
        pilih_operasi("×")

    elif karakter == "/":
        pilih_operasi("÷")

    elif tombol == "Return":
        hitung()

    elif tombol == "BackSpace":
        hapus_satu()

    elif tombol == "Escape":
        hapus_semua()


# window
root = tk.Tk()

root.title("RPC Calculator")
root.geometry("390x600")
root.resizable(False, False)

background = "#1e1e2f"
display_background = "#292941"
button_background = "#363653"
operator_background = "#4c4c78"
equal_background = "#6c63ff"

root.configure(bg=background)


# judul
judul = tk.Label(
    root,
    text="RPC CALCULATOR",
    font=("Arial", 22, "bold"),
    bg=background,
    fg="white"
)

judul.pack(pady=(25, 3))


# subjudul
subjudul = tk.Label(
    root,
    text="Sistem Terdistribusi",
    font=("Arial", 11),
    bg=background,
    fg="#b8b8c9"
)

subjudul.pack(pady=(0, 15))


# display
frame_display = tk.Frame(
    root,
    bg=display_background
)

frame_display.pack(
    padx=20,
    fill="x"
)


# ekspresi
label_ekspresi = tk.Label(
    frame_display,
    text="",
    font=("Arial", 13),
    bg=display_background,
    fg="#aaaabd",
    anchor="e"
)

label_ekspresi.pack(
    padx=15,
    pady=(12, 0),
    fill="x"
)


# hasil
display = tk.Entry(
    frame_display,
    font=("Arial", 30, "bold"),
    bg=display_background,
    fg="white",
    insertbackground="white",
    justify="right",
    bd=0
)

display.pack(
    padx=15,
    pady=(3, 15),
    ipady=8,
    fill="x"
)

display.insert(0, "0")


# tombol
frame_tombol = tk.Frame(
    root,
    bg=background
)

frame_tombol.pack(
    padx=20,
    pady=20,
    fill="both",
    expand=True
)


# membuat tombol
def buat_tombol(teks, baris, kolom, fungsi, warna=button_background):
    tombol = tk.Button(
        frame_tombol,
        text=teks,
        command=fungsi,
        font=("Arial", 15, "bold"),
        bg=warna,
        fg="white",
        activebackground=warna,
        activeforeground="white",
        bd=0,
        cursor="hand2"
    )

    tombol.grid(
        row=baris,
        column=kolom,
        padx=5,
        pady=5,
        sticky="nsew"
    )

    return tombol


# ukuran tombol
for i in range(4):
    frame_tombol.columnconfigure(i, weight=1)

for i in range(5):
    frame_tombol.rowconfigure(i, weight=1)


# baris 1
buat_tombol("C", 0, 0, hapus_semua)
buat_tombol("⌫", 0, 1, hapus_satu)
buat_tombol("÷", 0, 2, lambda: pilih_operasi("÷"), operator_background)
buat_tombol("×", 0, 3, lambda: pilih_operasi("×"), operator_background)

# baris 2
buat_tombol("7", 1, 0, lambda: tekan_angka("7"))
buat_tombol("8", 1, 1, lambda: tekan_angka("8"))
buat_tombol("9", 1, 2, lambda: tekan_angka("9"))
buat_tombol("-", 1, 3, lambda: pilih_operasi("-"), operator_background)

# baris 3
buat_tombol("4", 2, 0, lambda: tekan_angka("4"))
buat_tombol("5", 2, 1, lambda: tekan_angka("5"))
buat_tombol("6", 2, 2, lambda: tekan_angka("6"))
buat_tombol("+", 2, 3, lambda: pilih_operasi("+"), operator_background)

# baris 4
buat_tombol("1", 3, 0, lambda: tekan_angka("1"))
buat_tombol("2", 3, 1, lambda: tekan_angka("2"))
buat_tombol("3", 3, 2, lambda: tekan_angka("3"))
buat_tombol("=", 3, 3, hitung, equal_background)

# baris 5
buat_tombol("0", 4, 0, lambda: tekan_angka("0"))
buat_tombol(",", 4, 1, tekan_koma)


# keyboard
root.bind("<Key>", keyboard)

root.focus_force()


# jalankan aplikasi
root.mainloop()