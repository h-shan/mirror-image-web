from datetime import datetime

import requests
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

messages = []

@app.route('/')
def chat():
    return render_template('index.html', messages=messages)

@socketio.on('send message')
def send_message(message_text):
    message = message_text['data']
    res = requests.post('https://google.com', \
            json={'message': message}).content.decode()
    print('google ', res)
    if res:
        # messages.append(['chatbot', 'CPU', r, datetime.now().strftime('%h. %d, %Y. %I:%M:%S %p')])
        message_time = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
        socketio.emit('server', {'message': res, 'sender': 'CPU', 'class': 'chatbot', 'time': message_time}) 

if __name__ == '__main__':
    socketio.run(app)
