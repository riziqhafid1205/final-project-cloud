from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'lib_admin',
    'password': 'password_kuat',
    'database': 'db_server1'
}

def get_db():
    return mysql.connector.connect(**db_config)

@app.route('/fiksi', methods=['GET'])
def get_data():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM fiksi")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/fiksi', methods=['POST'])
def add_data():
    new_data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO fiksi (judul, penulis) VALUES (%s, %s)", (new_data['judul'], new_data['penulis']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Data Fiksi ditambahkan di Server 1"}), 201

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
