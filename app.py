import os
import asyncio
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from telethon import TelegramClient

loop = asyncio.get_event_loop()

load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')

client = TelegramClient('anom', api_id, api_hash)
app = Flask(__name__)
CORS(app)


async def send_data(data: dict):
    await client.send_message('me', "\n".join([f"{key}: {value}" for key, value in data.items()]))


@app.route("/")
def hello_world():
    return "<p>Hello, Flask!</p>"


@app.route('/submit', methods=['POST'])
def submit():
    print('Got a form!')
    data = request.form.to_dict()
    loop.run_until_complete(send_data(data))
    return jsonify(message='FormData received successfully')


if __name__ == '__main__':
    client.start()
    app.run(host='0.0.0.0', port=5000)
