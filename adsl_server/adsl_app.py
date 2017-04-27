# encoding: utf-8
from flask import Flask, request
import os
# Initialize the Flask application
app = Flask(__name__)
# Default route, print user's IP


@app.route('/api/get_ip', methods=['POST'])
def get_ip():

  ip = request.remote_addr
  return ip


@app.route('/api/restart_adsl', methods=['POST'])
def restart():
    try:
        cmd_stop = "pppoe-stop"
        cmd_start = "pppoe-start"
        os.system(cmd_stop)
        os.system(cmd_start)
        ip = request.remote_addr
        return ip
    except Exception as e:
        return e


if __name__ == '__main__':
  app.run(
        host="0.0.0.0",
        port=int("8000")
  )

