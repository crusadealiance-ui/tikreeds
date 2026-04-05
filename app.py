from flask import Flask, render_template, request
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')

    if not url:
        return "Masukkan URL"

    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')

        return f'''
        <h3>Link Video:</h3>
        <a href="{video_url}" target="_blank">Download Video</a>
        '''

    except Exception as e:
        return f"Error: {str(e)}"


import os
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
