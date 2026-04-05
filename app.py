from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir():
        if file.startswith('video'):
            return send_file(file, as_attachment=True)

    return "Download gagal"

import os
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    import os

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))