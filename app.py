import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from telethon import TelegramClient
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
port = int(os.getenv('PORT', 5000))

client = TelegramClient('anom', api_id, api_hash)
loop = client.loop

app = Flask(__name__)
CORS(app)


# Set Content Security Policy (CSP) headers
@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = ("default-src 'self'; connect-src 'self' "
                                                   "https://fishka-server.onrender.com:5000")
    return response


# Create a thread pool executor for running async tasks
executor = ThreadPoolExecutor(max_workers=1)


async def send_telegram_message(message):
    await client.connect()
    await client.send_message('me', message)
    await client.disconnect()


def send_telegram_message_sync(message):
    loop.run_until_complete(send_telegram_message(message))


@app.route("/")
def hello_world():
    return "<p>Hello, Flask!</p>"


@app.route('/submit', methods=['POST'])
def submit():
    print('Got a form!')
    data = request.form.to_dict()
    message = "\n".join([f"{key}: {value}" for key, value in data.items()])

    # Run the async function in a separate thread
    executor.submit(send_telegram_message_sync, message)

    return jsonify(message='FormData received successfully')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)