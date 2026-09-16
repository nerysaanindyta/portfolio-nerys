import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

app = Flask(__name__)

CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_PATH', 'credentials.json')
SPREADSHEET_NAME = os.getenv('SPREADSHEET_NAME', 'Data Pesan Portofolio')

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

def get_sheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    return client.open(SPREADSHEET_NAME).sheet1




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()
        nama = data.get('nama')
        email = data.get('email')
        pesan = data.get('pesan')

        if not nama or not email or not pesan:
            return jsonify({'status': 'error', 'message': 'Semua field wajib diisi!'}), 400

        sheet = get_sheet()
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([waktu, nama, email, pesan])

        return jsonify({'status': 'success', 'message': 'Pesan berhasil terkirim!'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
