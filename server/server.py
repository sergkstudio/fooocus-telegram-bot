from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/telegram/message', methods=['POST'])
def telegram_message():
    data = request.json
    print(f"Received message: {json.dumps(data)}")
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
