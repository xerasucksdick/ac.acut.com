from flask import Flask, request, render_template, jsonify
import requests
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_webhook():
    webhook_url = request.form.get('webhook_url')
    username = request.form.get('username')
    message = request.form.get('message')
    avatar_url = None
    if 'avatar' in request.files:
        avatar = request.files['avatar']
        if avatar.filename:
            filename = secure_filename(avatar.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            avatar.save(filepath)
            avatar_url = request.host_url + filepath.replace('\\', '/')
    data = {
        'username': username,
        'content': message,
    }
    if avatar_url:
        data['avatar_url'] = avatar_url
    resp = requests.post(webhook_url, json=data)
    return jsonify({'status': resp.status_code, 'response': resp.text})

if __name__ == '__main__':
    app.run(debug=True)
