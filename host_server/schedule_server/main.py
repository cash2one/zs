from flask import request, Flask, Response
import config
from functools import wraps
import requests
import time
import json


def check_auth(username, password):
    if config.NEED_AUTH:
        return username == config.AUTH_USER and password == config.AUTH_PASSWORD
    else:
        return True


def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password):
                return authenticate()
            return f(*args, **kwargs)
        except Exception as e:
            print(e)
    return decorated

app = Flask(__name__)



@app.route('/update_spider', methods=['GET'])
@requires_auth
def send_update():
    try:
        with open("scrapyd_url", 'r') as f:
            url_get = f.read().strip()
            f.close()
        url = "http://" + url_get + "/"
        project_response = requests.get(url + "listprojects.json")
        project_content = project_response.content
        project_json = json.loads(project_content)
        projects = project_json["projects"]
        for project_name in projects:
            spider_response = requests.get(url + "listspiders.json?project=" + project_name)
            spider_content = spider_response.content
            spider_json = json.loads(spider_content)
            spiders = spider_json["spiders"]
            for spider_name in spiders:
                param = {'project': project_name, 'spider': spider_name}
                schedule_response = requests.post(url + "schedule.json", params=param)
                print(schedule_response.content)
                with open('spider_time', 'r') as f:
                    time_get = f.read().strip()
                    f.close()
                time_int = int(time_get)
                time.sleep(time_int)
        return "ok"
    except Exception as e:
        print(e)


@app.route('/change/scrapyd_url/<url>', methods=['GET'])
@requires_auth
def change_url(url):
    try:
        with open('scrapyd_url', 'w') as f:
            f.write(url)
            f.close()
        return url + '\n'
    except Exception as e:
        print(e)


@app.route('/change/spider_time/<time_int>', methods=['GET'])
@requires_auth
def change_time(time_int):
    try:
        with open('spider_time', 'w') as f:
            f.write(time_int)
            f.close()
        return time_int + '\n'
    except Exception as e:
        print(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5888)

