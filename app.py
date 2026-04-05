from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Halaman utama
@app.route('/')
def index():
    return render_template('index.html')


# Proses download
@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')

    if not url:
        return "URL tidak ditemukan"

    try:
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': 'video.%(ext)s',
            'noplaylist': True,
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Cari file hasil download
        for file in os.listdir():
            if file.startswith('video'):
                return send_file(file, as_attachment=True)

        return "Gagal menemukan file"

    except Exception as e:
        return f"Error: {str(e)}"


# WAJIB untuk Railway
import os
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
