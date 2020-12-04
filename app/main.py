from flask import Flask, render_template
import sys
import json
sys.path.append("../..")
from app.vk_modules import vk_user_subscriptions

app = Flask(__name__)

with open('config.json') as json_file:
    data = json.load(json_file)
    for p in data['keys']:
        app.secret_key = p['app_secret_key']

app.register_blueprint(vk_user_subscriptions.bp)

@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
