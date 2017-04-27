FROM tiangolo/uwsgi-nginx:python3.5
#FROM python:3.5

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

#COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./nginx.conf /etc/nginx/conf.d/nginx.conf

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

CMD python main.py