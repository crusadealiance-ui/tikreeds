from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Halaman utama
@app.route('/')
def index():
    return render_template('index.html')


# Download video
@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')

    if not url:
        return "Masukkan URL"

    try:
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': '/tmp/video.%(ext)s',
            'noplaylist': True,
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Cari file di /tmp
        for file in os.listdir('/tmp'):
            if file.startswith('video'):
                return send_file(f'/tmp/{file}', as_attachment=True)

        return "Gagal download"

    except Exception as e:
        return f"Error: {str(e)}"


# WAJIB untuk Railway
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
