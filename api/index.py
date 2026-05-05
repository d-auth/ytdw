from flask import Flask, request, jsonify
from flask_cors import CORS
from pytubefix import YouTube
import traceback

app = Flask(__name__)
CORS(app)

@app.route('/api/test')
def test():
    return jsonify({"status": "API está funcionando!", "biblioteca": "pytubefix"})

@app.route('/api/info')
def get_info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL não fornecida"}), 400
    
    try:
        # ANDROID_VR costuma ser o cliente mais difícil de o YouTube bloquear
        yt = YouTube(url, client='ANDROID_VR')
        
        streams = []
        # Tenta pegar os formatos MP4
        for stream in yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc():
            streams.append({
                "itag": stream.itag,
                "resolution": stream.resolution,
                "size": round(stream.filesize / (1024 * 1024), 2),
                "url": stream.url
            })
            
        return jsonify({
            "title": yt.title,
            "thumbnail": yt.thumbnail_url,
            "author": yt.author,
            "streams": streams
        })
    except Exception as e:
        # Se falhar, vamos retornar o erro exato para você ler
        return jsonify({
            "error": "O YouTube bloqueou o acesso do servidor",
            "details": str(e)
        }), 500

