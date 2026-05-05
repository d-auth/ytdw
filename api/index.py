from flask import Flask, request, jsonify
from flask_cors import CORS
from pytubefix import YouTube
import traceback

app = Flask(__name__)
CORS(app)

# ROTA DE TESTE - Acesse /api/test no navegador
@app.route('/api/test')
def test():
    return jsonify({"status": "API está funcionando!", "biblioteca": "pytubefix"})

@app.route('/api/info')
def get_info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL não fornecida"}), 400
    
    try:
        # Tentativa com cliente WEB_CREATOR que às vezes é mais estável
        yt = YouTube(url, client='WEB_CREATOR')
        
        streams = []
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
            "streams": streams
        })
    except Exception as e:
        error_msg = str(e)
        print(f"ERRO: {error_msg}")
        return jsonify({
            "error": "Erro ao buscar vídeo",
            "details": error_msg,
            "trace": traceback.format_exc()
        }), 500
