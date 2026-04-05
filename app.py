from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

app = Flask(__name__)


# =========================
# ROUTE HOME
# =========================
@app.route('/')
def index():
    return render_template('index.html')


# =========================
# ROUTE DOWNLOAD (API)
# =========================
@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')

    if not url:
        return jsonify({"error": "URL tidak boleh kosong"})

    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'nocheckcertificate': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # Ambil link video terbaik
            video_url = None

            if 'url' in info:
                video_url = info['url']
            elif 'formats' in info:
                for f in info['formats']:
                    if f.get('url'):
                        video_url = f['url']
                        break

            thumbnail = info.get('thumbnail', '')

        if not video_url:
            return jsonify({"error": "Gagal mengambil video"})

        return jsonify({
            "status": "success",
            "video": video_url,
            "thumbnail": thumbnail
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        })


# =========================
# HEALTH CHECK (OPSIONAL)
# =========================
@app.route('/health')
def health():
    return "OK"


# =========================
# RUN (WAJIB UNTUK RAILWAY)
# =========================
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get("PORT", 5000))
    )
