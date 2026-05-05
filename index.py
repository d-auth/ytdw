from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from pytubefix import YouTube
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/info', methods=['GET'])
def get_info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Nenhuma URL fornecida"}), 400
    
    try:
        # Usando pytubefix para contornar problemas comuns do pytube
        yt = YouTube(url)
        
        # Filtra apenas streams progressivos (vídeo + áudio juntos) para facilitar o download direto
        streams = []
        for stream in yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc():
            streams.append({
                "itag": stream.itag,
                "resolution": stream.resolution,
                "mime_type": stream.mime_type,
                "size": round(stream.filesize / (1024 * 1024), 2), # MB
                "url": stream.url
            })
        
        return jsonify({
            "title": yt.title,
            "thumbnail": yt.thumbnail_url,
            "duration": yt.length,
            "author": yt.author,
            "streams": streams
        })
    except Exception as e:
        print(f"Erro: {str(e)}")
        return jsonify({"error": "Não foi possível buscar as informações do vídeo. Verifique se a URL está correta."}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

# O Vercel espera que a variável 'app' esteja no escopo global
if __name__ == '__main__':
    app.run(debug=True)
