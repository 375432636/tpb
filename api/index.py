import json
from datetime import datetime

from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

tracker = "&tr=udp://tracker.coppersurfer.tk:6969/announce&tr=udp://tracker.openbittorrent.com:6969/announce&tr=udp://tracker.bittor.pw:1337/announce&tr=udp://tracker.opentrackr.org:1337&tr=udp://bt.xxx-tracker.com:2710/announce&tr=udp://public.popcorn-tracker.org:6969/announce&tr=udp://eddie4.nl:6969/announce&tr=udp://tracker.torrent.eu.org:451/announce&tr=udp://p4p.arenabg.com:1337/announce&tr=udp://tracker.tiny-vps.com:6969/announce&tr=udp://open.stealth.si:80/announce"

def search(data):
    keyword = data["keyword"]
    name_filter = data.get("name_filter")
    user_filter = data.get("user_filter")
    url = f"https://apibay.org/q.php?q={keyword}&cat=0"
    r = requests.get(url)
    JSON = r.json()
    if name_filter:
        JSON = [i for i in JSON if name_filter in i['name']]
    if user_filter:
        JSON = [i for i in JSON if user_filter in i['username']]
    for i in JSON:
        magnet_link =f"magnet:?xt=urn:btih:{i['info_hash']}&dn={i['name']}{tracker}"
        i["magnet_link"] = magnet_link
        i['added'] = datetime.fromtimestamp(int(i['added'])).strftime("%Y-%m-%d")
    return JSON

@app.route('/tpb',methods = ['GET'])
def tpb():
    data = request.args
    JSON = search(data)
    JSON = json.dumps(JSON)
    # return jsonify(JSON)
    with open("./api/templates/table.html","r") as f:
        text = f.read()

    return text.replace("{{tableData}}",JSON)

if __name__ == '__main__':
    app.run()