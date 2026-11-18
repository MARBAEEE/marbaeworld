import os
import tempfile
from flask import Flask, render_template, request, send_file, jsonify
from pdf2docx import Converter

app = Flask(__name__)

# Halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Jalur untuk menerima file PDF dan mengubahnya menjadi Word
@app.route('/convert', methods=['POST'])
def convert_pdf_to_word():
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file yang diunggah'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nama file kosong'}), 400
        
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Format file harus PDF (.pdf)'}), 400

    try:
        # Simpan PDF sementara di folder temp sistem
        temp_dir = tempfile.mkdtemp()
        pdf_path = os.path.join(temp_dir, file.filename)
        file.save(pdf_path)

        # Tentukan nama file output (.docx)
        docx_filename = os.path.splitext(file.filename)[0] + '.docx'
        docx_path = os.path.join(temp_dir, docx_filename)

        # Proses konversi PDF ke Word menggunakan pdf2docx
        cv = Converter(pdf_path)
        cv.convert(docx_path, start=0, end=None)
        cv.close()

        # Kirim file Word yang sudah jadi ke browser pengguna
        return send_file(
            docx_path,
            as_attachment=True,
            download_name=docx_filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except Exception as e:
        return jsonify({'error': f'Gagal mengonversi file: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)