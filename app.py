import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from telethon import TelegramClient

load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
port = int(os.getenv('PORT', 5000))

client = TelegramClient('anom', api_id, api_hash)
loop = client.loop

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return "<p>Hello, Flask!</p>"


@app.route('/submit', methods=['POST'])
async def submit():
    print('Got a form!')
    data = request.form.to_dict()
    message = "\n".join([f"{key}: {value}" for key, value in data.items()])

    await client.connect()
    await client.send_message('me', message)

    return jsonify(message='FormData received successfully')


if __name__ == '__main__':
    loop.run_until_complete(app.run(host='0.0.0.0', port=port))
