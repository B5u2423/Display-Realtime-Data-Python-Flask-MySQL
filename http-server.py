import http.server
import socketserver
from urllib.parse import parse_qs
import mysql.connector
from config import MYSQL_CONFIG # import credentials

PORT = 8090

"""
Please read the `config.py`
"""

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_POST(self):
        # add header
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        # parse payload
        data = parse_qs(post_data)
        temperature = data.get('temperature', [None])[0]
        humidity = data.get('humidity', [None])[0]
        print(f"Received data from ESP32: {data}")

        temperature = float(temperature)
        humidity = float(humidity)
        
        # connect to mysql
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        # database query to insert data
        cursor.execute("INSERT INTO sensor_data (temperature, humidity) VALUES (%s, %s)", (temperature, humidity))

        # commit and close connection
        conn.commit()
        conn.close()
 
httpd = socketserver.TCPServer(("", PORT), MyHandler)
print(f"Server online on port {PORT}")

httpd.serve_forever()
