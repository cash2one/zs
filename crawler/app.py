# encoding: utf-8
from flask import Flask
from ximalaya import main
from flask import request, send_from_directory
import os
import socket
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

download_dir = 'ximalaya_downloads'

"""
接口文档

接口地址：localhost:8000/api/v1/sound or localhost:8000//api/v1/download/<path:filename>
请求方式：GET or POST
接口格式：{"url": url}
响应格式：'{"key": "success", "please_copy": url}" or "{"key": "failure", "please_copy": None}'
复制"please_copy"的url到浏览器即可下载


以上仅做示例
"""


def Get_local_ip():
    try:
        csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        csock.connect(('8.8.8.8', 80))
        (addr, port) = csock.getsockname()
        csock.close()
        return addr
    except socket.error:
        return "127.0.0.1"


@app.route('/api/v1/sound', methods=['POST'])
def crawler_ximalaya():
    r = request.get_json()
    url = r["url"]
    try:
        name = main(url,download_dir)
        ip_adress = Get_local_ip()
        n = str(name).decode("unicode-escape")
        if n.find('u') != -1:
            s = n.split('u')[1]
            key_name = s[1:-2]
        else:
            key_name = n[2:-2]
        key_url = ip_adress + ':8000/api/v1/download/' + key_name + '.m4a'
        a = '{"key": "success", "please_copy": %s}' % key_url
        return a
    except Exception as e:
        a = '{"key": "failure", "please_copy": None}'
        return a


dirpath = os.path.join(app.root_path, download_dir)


@app.route("/api/v1/download/<path:filename>")
def downloader(filename):
    print(filename)
    return send_from_directory(dirpath, filename, as_attachment=True)


if __name__ == '__main__':
    config = dict(
        host='0.0.0.0',
        port=8000,
    )
    app.run(**config)
