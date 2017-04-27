# encoding: utf-8
from flask import Flask
from ximalaya import main
from flask import request,jsonify,send_from_directory,abort,make_response,send_file
import os



# 先要初始化一个 Flask 实例
app = Flask(__name__)

"""
接口文档

接口地址：localhost:8000/sound
请求方式：POST
接口格式：{"url": url}
响应格式：'{"key": "success"}" or "{"key": "failure"}'



以上仅做示例
"""


@app.route('/sound', methods=['POST'])
def crawler_ximalaya():
    r = request.get_json()
    url = r["url"]
    if main(url):
        a = '{"key": "success"}'
        return a
    else:
        a = '{"key": "failure"}'
        return a


# @app.route('/download/<path:filename>', methods=['GET'])
# def download(filename):
#     now = os.getcwd()
#     get_filename = now + '/ximalaya/'
#     print('get_name', get_filename)
#     a = filename + '.m4a'
#     print('a',a)
#     b = '啦啦啦.m4a'
#     return send_from_directory(get_filename, b, as_attachment=True)

dirpath = os.path.join(app.root_path,'ximalaya')
@app.route("/download/<path:filename>")
def downloader(filename):
    a = filename.encode('latin-1', 'static')
    return send_from_directory(dirpath,a,as_attachment=True)

if __name__ == '__main__':
    config = dict(
        debug = True,
        host='0.0.0.0',
        port=8000,
    )
    app.run(**config)
