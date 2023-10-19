from flask import Flask,jsonify,request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/tpb',methods = ['GET'])
def tpb():
    data = request.args
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
    return jsonify(JSON)
if __name__ == '__main__':
    app.run()