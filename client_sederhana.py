import xmlrpc.client

# koneksi ke server
server = xmlrpc.client.ServerProxy("http://localhost:8000")


def format_hasil(hasil):
    if isinstance(hasil, str):
        return hasil

    if isinstance(hasil, float) and hasil.is_integer():
        hasil = int(hasil)

    if isinstance(hasil, int):
        return f"{hasil:,}".replace(",", ".")

    return str(hasil).replace(".", ",")


print("=== KALKULATOR RPC ===")

angka1 = float(input("Masukkan angka pertama: "))
angka2 = float(input("Masukkan angka kedua: "))

print("\nPilih operasi:")
print("1. Penjumlahan")
print("2. Pengurangan")
print("3. Perkalian")
print("4. Pembagian")

pilihan = input("Masukkan pilihan: ")

if pilihan == "1":
    hasil = server.tambah(angka1, angka2)
elif pilihan == "2":
    hasil = server.kurang(angka1, angka2)
elif pilihan == "3":
    hasil = server.kali(angka1, angka2)
elif pilihan == "4":
    hasil = server.bagi(angka1, angka2)
else:
    hasil = "Pilihan tidak valid"

print("Hasil:", format_hasil(hasil))