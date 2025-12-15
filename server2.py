from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'lib_admin',
    'password': 'password_kuat',
    'database': 'db_server2'
}

def get_db():
    return mysql.connector.connect(**db_config)

@app.route('/jurnal', methods=['GET'])
def get_data():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jurnal")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/jurnal', methods=['POST'])
def add_data():
    new_data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jurnal (judul, peneliti) VALUES (%s, %s)", (new_data['judul'], new_data['peneliti']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Data Jurnal ditambahkan di Server 2"}), 201

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)
