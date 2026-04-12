from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Halaman utama
@app.route('/')
def index():
    return render_template('index.html')


# Proses download
@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')

    if not url or url.strip() == '':
        return "❌ URL tidak boleh kosong.", 400

    # Nama file unik agar tidak bentrok jika banyak user
    filename = os.path.join(DOWNLOAD_FOLDER, f'video_{uuid.uuid4().hex}')

    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': filename + '.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'merge_output_format': 'mp4',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            ext = info.get('ext', 'mp4')

        filepath = filename + f'.{ext}'

        if not os.path.exists(filepath):
            # Coba cari file dengan nama yang cocok
            for f in os.listdir(DOWNLOAD_FOLDER):
                if f.startswith(os.path.basename(filename)):
                    filepath = os.path.join(DOWNLOAD_FOLDER, f)
                    break
            else:
                return "❌ Gagal menemukan file hasil download.", 500

        return send_file(
            filepath,
            as_attachment=True,
            download_name='tiktok_video.mp4',
            mimetype='video/mp4'
        )

    except yt_dlp.utils.DownloadError as e:
        return f"❌ Gagal mendownload video: {str(e)}", 400

    except Exception as e:
        return f"❌ Terjadi kesalahan: {str(e)}", 500


# Bersihkan file lama (opsional, bisa dipanggil manual)
@app.route('/cleanup', methods=['GET'])
def cleanup():
    count = 0
    for f in os.listdir(DOWNLOAD_FOLDER):
        try:
            os.remove(os.path.join(DOWNLOAD_FOLDER, f))
            count += 1
        except:
            pass
    return f"✅ {count} file dihapus."


# WAJIB untuk Railway
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))        return "Gagal menemukan file"

    except Exception as e:
        return f"Error: {str(e)}"


# WAJIB untuk Railway
import os
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
