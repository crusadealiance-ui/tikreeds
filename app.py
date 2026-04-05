from flask import Flask, render_template, request, jsonify, redirect
import yt_dlp
import os

app = Flask(__name__)


# ======================
# HOME
# ======================
@app.route('/')
def index():
    return render_template('index.html')


# ======================
# GET VIDEO LINK
# ======================
@app.route('/get-link', methods=['POST'])
def get_link():
    url = request.form.get('url')

    if not url:
        return jsonify({"error": "URL tidak boleh kosong"})

    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'format': 'best',
            'nocheckcertificate': True,
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0'
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

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
            return jsonify({"error": "Gagal ambil video"})

        return jsonify({
            "video": video_url,
            "thumbnail": thumbnail
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# ======================
# DOWNLOAD (1x klik)
# ======================
@app.route('/download')
def download():
    video_url = request.args.get('url')
    return redirect(video_url)


# ======================
# RUN (Railway)
# ======================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
