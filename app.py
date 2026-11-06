import os
import requests
from flask import Flask, render_template, request, Response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/proxy')
def proxy():
    video_url = request.args.get('url')
    if not video_url:
        return "No URL provided", 400

    try:
        # Stream the video from Telegram/External source
        req = requests.get(video_url, stream=True)
        return Response(
            req.iter_content(chunk_size=1024),
            status=req.status_code,
            headers=dict(req.headers)
        )
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
