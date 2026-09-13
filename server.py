from xmlrpc.server import SimpleXMLRPCServer

# membuat server
server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)

print("=================================")
print("      RPC CALCULATOR SERVER")
print("=================================")
print("Server berjalan di localhost:8000")
print("Menunggu permintaan dari client...")


# penjumlahan
def tambah(a, b):
    return a + b


# pengurangan
def kurang(a, b):
    return a - b


# perkalian
def kali(a, b):
    return a * b


# pembagian
def bagi(a, b):
    if b == 0:
        return "Tidak bisa dibagi dengan 0"
    return a / b


# daftar fungsi RPC
server.register_function(tambah, "tambah")
server.register_function(kurang, "kurang")
server.register_function(kali, "kali")
server.register_function(bagi, "bagi")


# menjalankan server
server.serve_forever()