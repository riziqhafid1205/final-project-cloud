from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# URL Server Internal (Tetap HTTP karena satu mesin)
SERVER_1_URL = "http://127.0.0.1:5001/fiksi"
SERVER_2_URL = "http://127.0.0.1:5002/jurnal"

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Gateway Ready via Nginx (HTTP)"})

@app.route('/api/all-products', methods=['GET'])
def get_all_products():
    combined_data = []
    status_report = {}

    # --- AMBIL DATA SERVER 1 ---
    try:
        response1 = requests.get(SERVER_1_URL, timeout=2)
        if response1.status_code == 200:
            data1 = response1.json()
            for item in data1:
                item['source'] = 'Server 1 (Fiksi)'
            combined_data.extend(data1)
            status_report['server_1'] = 'Online'
        else:
            status_report['server_1'] = f'Error {response1.status_code}'
    except Exception as e:
        print(f"Server 1 Error: {e}")
        status_report['server_1'] = 'Offline/Down'

    # --- AMBIL DATA SERVER 2 ---
    try:
        response2 = requests.get(SERVER_2_URL, timeout=2)
        if response2.status_code == 200:
            data2 = response2.json()
            for item in data2:
                item['source'] = 'Server 2 (Jurnal)'
            combined_data.extend(data2)
            status_report['server_2'] = 'Online'
        else:
            status_report['server_2'] = f'Error {response2.status_code}'
    except Exception as e:
        print(f"Server 2 Error: {e}")
        status_report['server_2'] = 'Offline/Down'

    return jsonify({
        "status": status_report,
        "data": combined_data
    })

if __name__ == '__main__':
    # PERUBAHAN DI SINI:
    # Hapus "ssl_context='adhoc'"
    # Biarkan berjalan di HTTP biasa, karena Nginx nanti yang urus HTTPS/Port 80
    app.run(host='0.0.0.0', port=5000)
