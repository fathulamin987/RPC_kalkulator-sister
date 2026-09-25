from flask import Flask, jsonify, request
import xmlrpc.client

app = Flask(__name__)

# Hubungkan ke RPC Server Anda (sesuaikan port jika server.py Anda menggunakan port lain)
RPC_SERVER_URL = "http://localhost:8000/"

@app.route('/api/hitung', methods=['POST'])
def api_hitung():
    data = request.json
    angka1 = data.get('angka1')
    angka2 = data.get('angka2')
    operasi = data.get('operasi') # misal: 'tambah', 'kurang', dsb.

    try:
        # Client API bertindak sebagai RPC Client untuk memanggil fungsi di server.py
        proxy = xmlrpc.client.ServerProxy(RPC_SERVER_URL)
        
        # Memanggil fungsi remote di server.py (sesuaikan dengan nama fungsi di server Anda)
        # Contoh: hasil = proxy.tambah(angka1, angka2)
        hasil = proxy.tambah(angka1, angka2) 

        return jsonify({
            "status": "success",
            "message": "Berhasil memproses via RPC",
            "hasil": hasil
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Gagal menghubungi RPC Server: {str(e)}"
        }, 500)

if __name__ == '__main__':
    print("🌐 REST API Gateway berjalan di http://localhost:5000")
    app.run(port=5000, debug=True)