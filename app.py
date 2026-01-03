from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import subprocess
import uuid
import os
import requests

app = Flask(__name__)
CORS(app)

@app.route('/combine', methods=['POST'])
def combine_video_audio():
    try:
        data = request.get_json()
        video_url = data.get('video_url')
        audio_url = data.get('audio_url')
        
        if not video_url or not audio_url:
            return jsonify({'error': 'video_url and audio_url required'}), 400
        
        video_path = f"/tmp/video_{uuid.uuid4()}.mp4"
        audio_path = f"/tmp/audio_{uuid.uuid4()}.mp3"
        output_path = f"/tmp/output_{uuid.uuid4()}.mp4"
        
        video_response = requests.get(video_url, timeout=60)
        with open(video_path, 'wb') as f:
            f.write(video_response.content)
        
        audio_response = requests.get(audio_url, timeout=60)
        with open(audio_path, 'wb') as f:
            f.write(audio_response.content)
        
        command = [
            'ffmpeg', '-i', video_path, '-i', audio_path,
            '-c:v', 'copy', '-c:a', 'aac', '-shortest', '-y', output_path
        ]
        
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            return jsonify({'error': f'FFmpeg error: {result.stderr}'}), 500
        
        os.remove(video_path)
        os.remove(audio_path)
        
        return send_file(output_path, mimetype='video/mp4', as_attachment=True, download_name='final_video.mp4')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/', methods=['GET'])
def home():
    return jsonify({'service': 'Video Combiner API', 'status': 'running'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

3. Click **"Commit changes"** (botón verde arriba a la derecha)

---

### **ARCHIVO 2: requirements.txt**

1. Click aquí:
```
https://github.com/miguelserrsanfran-boop/video-combiner-api/new/main?filename=requirements.txt
```

2. Pega:
```
flask==3.0.0
flask-cors==4.0.0
requests==2.31.0
```

3. Click **"Commit changes"**

---

### **ARCHIVO 3: Dockerfile**

1. Click aquí:
```
  FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
https://github.com/miguelserrsanfran-boop/video-combiner-api/new/main?filename=Dockerfile
