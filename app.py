from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Menggunakan API TikWM sebagai jembatan data
TIKTOK_API_URL = "https://www.tikwm.com/api/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch_music():
    video_url = request.form.get('url')
    if not video_url:
        return jsonify({"error": "URL tidak boleh kosong"}), 400

    try:
        response = requests.get(TIKTOK_API_URL, params={'url': video_url})
        data = response.json()

        if data.get('code') == 0:
            music_data = {
                "title": data['data']['music_info']['title'],
                "author": data['data']['music_info']['author'],
                "audio_url": data['data']['music'],
                "cover": data['data']['music_info']['cover']
            }
            return jsonify(music_data)
        else:
            return jsonify({"error": "Gagal mengambil data. Link salah atau video privat."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
