import os
import sys
import json
from datetime import datetime

import requests
from flask import Flask, request, session, redirect, url_for, render_template, flash, make_response
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

messages = [] # message = [['sender', 'name', 'msg', 'time']]

@app.route('/')
def chat():
    return render_template('index.html', messages=messages)


# @app.route('/', methods=['POST'])
# def send1():
#     message = request.form['msg']
#     if message != "":
#         messages.append(['user', 'You', message, datetime.now().strftime("%h. %d, %Y. %I:%M:%S %p")])
#         send_message(message)

#     return redirect(url_for('chat'))

# def send_message(message_text):
#     r = requests.post('https://mirror-image.herokuapp.com', json = {'message': message_text}).content.decode()
#     if r != "":
#         messages.append(['chatbot', 'CPU', r, datetime.now().strftime("%h. %d, %Y. %I:%M:%S %p")])
#     return r

@socketio.on('send message')
def send_message(message_text):
    message_text = message_text['data']
    r = requests.post('https://mirror-image.herokuapp.com', json = {'message': message_text}).content.decode()
    if r != "":
        # messages.append(['chatbot', 'CPU', r, datetime.now().strftime("%h. %d, %Y. %I:%M:%S %p")])
        socketio.emit('server', {'message': r, "sender": "CPU", "class":"chatbot", "time": datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")}) 

if __name__ == '__main__':
    socketio.run(app)
