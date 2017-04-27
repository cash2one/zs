from flask import request, Flask, Response
import config
from functools import wraps
import requests
import time
import json


app = Flask(__name__)



@app.route('/update_spider/<key>', methods=['GET'])
def send_update(key):
    try:
        if key == config.KEY:
            with open('scrapyd_url', 'r') as f:
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
                    schedule_response = requests.get("http://localhost:5999/update_spider/" + key + "/" + project_name + "/" + spider_name)
                    print(schedule_response.content)
                    with open('spider_time', 'r') as f:
                        time_get = f.read().strip()
                        f.close()
                    time_int = int(time_get)
                    time.sleep(time_int)
            return "ok"
        else:
            return 'Invalid Key'
    except Exception as e:
        print(e)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5888)

