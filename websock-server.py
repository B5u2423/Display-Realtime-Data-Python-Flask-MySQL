from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import mysql.connector
from config import MYSQL_CONFIG
from datetime import timedelta
from threading import Lock

app = Flask(__name__)
socketio = SocketIO(app)
latest_id = None # latest entry id

thread = None
thread_lock = Lock()

"""
Please read the `config.py`
"""

#--------------------------------------------------------#

def query_database():
    """
    Making a query to the database. Only getting the latest entry
    - No param
    
    Returns: 
    A list consists of 2 elements: `id` and a `payload` dictionary.
    """
    # connect to MySQL
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    # get the latest entry
    cursor.execute("SELECT id, time, temperature, humidity FROM sensor_data ORDER BY id DESC LIMIT 1")
    data = cursor.fetchone()

    # close conn
    cursor.close()
    conn.close()

    tmp_id = data[0]
    tmp_time = str(data[1])
    tmp_temperature = data[2]
    tmp_humidity = data[3]

    payload = [tmp_id, {'labels': tmp_time, 'temperature': tmp_temperature, 'humidity': tmp_humidity}]

    return payload

#------------------------------------------------------#

@app.route('/')
def index():
    return render_template('index.html')

#------------------------------------------------------#

@app.route('/history')
def get_history():
    # connect to MySQL 
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT date, time, humidity, temperature FROM sensor_data")
    data = cursor.fetchall()

    # close conn
    cursor.close()
    conn.close()

    # pass data to `history.html`
    return render_template('history.html', data=data)

#------------------------------------------------------#

def background_thread():
    global latest_id

    # init `latest_id`
    latest_id = query_database()[0]
    curr_id = None
    
    while True:
        payload = query_database()
        curr_id = payload[0]

        # only emit data `if`
        if (curr_id > latest_id):
            print(f"Pload sent:  {payload}")
            # print(f"latest: {latest_id}") # for debugging
            # print(f"curr:   {curr_id}")
            socketio.emit('update_data', payload[1])
            latest_id = curr_id 

        socketio.sleep(1) # set interval between each queries
       
#------------------------------------------------------#

@socketio.on('connect')
def connect():
    global thread

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

#------------------------------------------------------#

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

#------------------------ main ------------------------#
if __name__ == '__main__':
    socketio.run(app, debug=True, port=8091)