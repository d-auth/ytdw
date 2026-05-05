from flask import Flask, request, jsonify
from flask_cors import CORS
from pytubefix import YouTube
import traceback

app = Flask(__name__)
CORS(app)

@app.route('/api/info')
def get_info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL não fornecida"}), 400
    
    try:
        # Usamos client='MWEB' para simular um navegador mobile (costuma evitar bloqueios)
        yt = YouTube(url, client='MWEB')
        
        streams = []
        # Pegamos apenas MP4 progressivo (vídeo + áudio)
        for stream in yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc():
            streams.append({
                "itag": stream.itag,
                "resolution": stream.resolution,
                "size": round(stream.filesize / (1024 * 1024), 2),
                "url": stream.url
            })
            
        if not streams:
             return jsonify({"error": "Nenhum formato compatível encontrado. Tente outro vídeo."}), 404

        return jsonify({
            "title": yt.title,
            "thumbnail": yt.thumbnail_url,
            "duration": yt.length,
            "author": yt.author,
            "streams": streams
        })
    except Exception as e:
        # Isso vai imprimir o erro exato nos logs do Vercel
        print(traceback.format_exc())
        # E isso vai te mostrar o erro no console do navegador
        return jsonify({
            "error": "Erro no Servidor",
            "details": str(e)
        }), 500

app.debug = True
