import subprocess
import threading
import shutil
import os
from quart import Quart, request, jsonify, render_template
from static_bp import static

app = Quart(__name__, "/static", static_folder=None)
app.register_blueprint(static, url_prefix='/static')

@app.route("/api/download", methods=['POST'])
async def download():
    request_json = await request.get_json()
    print(request_json)
    try:
        if request_json["download_audio"]:
            type_flag = " -x "
        else:
            type_flag = ""
    except TypeError:
        return jsonify({
            "error": "bad_request"
        }), 400
    if os.name != 'nt':
        ytdl = subprocess.run(f"./youtube-dl -o static/%(id)s.%(ext)s {type_flag} {request_json['video_url']}",
                              capture_output=True)
    else:
        ytdl = subprocess.run(f"youtube-dl.exe -o static/%(id)s.%(ext)s {type_flag} {request_json['video_url']}",
                              capture_output=True)
    stdout_lines = ytdl.stdout.split(b"\n")
    print(stdout_lines)
    if b"already been downloaded" in stdout_lines[1]:
        return "This shouldn't happen!"
    try:
        file_path = stdout_lines[1].split(b": ")[1].decode()
        file_path_in_static = file_path.split("static\\")[1]
    except:
        return "Not a YouTube URL!"

    """@after_this_request
    async def remove_file(response):
        os.remove(file_path)"""
    return jsonify({
        "error": "none",
        "download_url": "http://127.0.0.1:5000/static/" + file_path_in_static
    })

@app.route("/")
@app.route("/index")
@app.route("/index.html")
async def index():
    return await render_template("index.html")

@app.route("/script.js")
async def script():
    return await render_template("script.js")

def cleanup():
    print("Cleanup task started!")
    while True:
        shutil.rmtree("static")
        os.mkdir("static")
        import time
        print("Cleanup task running!")
        time.sleep(18000)


t = threading.Thread(target=cleanup, args=[])
t.setDaemon(False)
t.start()

app.run()
