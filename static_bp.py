from quart import Blueprint, request
import threading
import time
import os

static = Blueprint('static', __name__, static_url_path="/", static_folder="static")

@static.after_request
async def after_request_func(response):
    if response.status_code == 200:
        file_path = request.base_url.replace("http://localhost:5000/", "")
        t = threading.Thread(target=delete_after_request_thread, args=[file_path])
        t.setDaemon(False)
        t.start()
    return response

def delete_after_request_thread(file_path):
    time.sleep(2000)
    os.remove(file_path)
