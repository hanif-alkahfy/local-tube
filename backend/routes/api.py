from flask import Flask, request, jsonify, send_file, Response, Blueprint, abort
from yt_dlp import YoutubeDL
from werkzeug.utils import safe_join
import urllib.parse
import os
import re
import uuid
import json
import subprocess

api = Blueprint("api", __name__)

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# --- Fungsi untuk membuat thumbnail dari video ---
def generate_thumbnail(video_path, thumbnail_path):
    try:
        subprocess.run([
            'ffmpeg',
            '-i', video_path,
            '-ss', '00:00:01.000',
            '-vframes', '1',
            thumbnail_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error generating thumbnail: {e}")

# Test route to check if the API is running
@api.route("/ping")
def ping():
    return {"status": "ok"}

# Route to handle video download requests
@api.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')
    resolution = data.get('resolution', '720p')

    if not url:
        return jsonify({"error": "URL is required"}), 400

    video_id = str(uuid.uuid4())
    info = {}

    def progress_hook(d):
        if d['status'] == 'finished':
            info.update(d.get('info_dict', {}))

    output_template = os.path.join(DOWNLOAD_FOLDER, f'{video_id}.%(ext)s')

    format_selector = {
        '1080p': 'bv*[height<=1080]+ba/best',
        '720p': 'bv*[height<=720]+ba/best',
        '480p': 'bv*[height<=480]+ba/best',
        '360p': 'bv*[height<=360]+ba/best'
    }

    ydl_opts = {
        'outtmpl': output_template,
        'format': format_selector.get(resolution, 'best'),
        'progress_hooks': [progress_hook],
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }]
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if info:
            video_filename = f"{video_id}.mp4"
            video_path = os.path.join(DOWNLOAD_FOLDER, video_filename)
            thumbnail_filename = f"{video_id}.jpg"
            thumbnail_path = os.path.join(DOWNLOAD_FOLDER, thumbnail_filename)
            generate_thumbnail(video_path, thumbnail_path)

            metadata = {
                'id': video_id,
                'title': info.get('title', 'Untitled'),
                'filename': video_filename,
                'thumbnail': thumbnail_filename
            }
            with open(os.path.join(DOWNLOAD_FOLDER, f'{video_id}.json'), 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False)

        return jsonify({"message": "Download success", "id": video_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to see video files
@api.route('/videos', methods=['GET'])
def list_videos():
    videos = []
    for file in os.listdir(DOWNLOAD_FOLDER):
        if file.endswith('.json'):
            metadata_path = os.path.join(DOWNLOAD_FOLDER, file)
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            videos.append({
                "id": metadata.get("id"),
                "title": metadata.get("title"),
                "filename": metadata.get("filename"),
                "path": f"/api/stream/{metadata.get('id')}",
                "thumbnail": f"/api/thumbnails/{metadata.get('thumbnail')}" if metadata.get("thumbnail") else None
            })

    return jsonify({"videos": videos})

# Route to serve thumbnail images
@api.route('/thumbnails/<filename>')
def get_thumbnail(filename):
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        return send_file(filepath, mimetype='image/jpeg')
    else:
        abort(404)

# Route to stream video files
@api.route('/stream/<video_id>', methods=['GET'])
def stream_video(video_id):
    json_path = os.path.join(DOWNLOAD_FOLDER, f"{video_id}.json")
    if not os.path.isfile(json_path):
        return abort(404, description="Metadata not found")

    with open(json_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    filename = metadata.get('filename')
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    if not os.path.isfile(filepath):
        return abort(404, description="Video not found")

    range_header = request.headers.get('Range', None)
    if not range_header:
        return send_file(filepath, as_attachment=False)

    size = os.path.getsize(filepath)
    byte1, byte2 = 0, None

    match = re.search(r'bytes=(\d+)-(\d*)', range_header)
    if match:
        g = match.groups()
        byte1 = int(g[0])
        if g[1]:
            byte2 = int(g[1])

    length = size - byte1
    if byte2 is not None:
        length = byte2 - byte1 + 1

    with open(filepath, 'rb') as f:
        f.seek(byte1)
        data = f.read(length)

    rv = Response(data,
                  206,
                  mimetype="video/mp4",
                  content_type="video/mp4",
                  direct_passthrough=True)
    rv.headers.add('Content-Range', f'bytes {byte1}-{byte1 + length - 1}/{size}')
    return rv
