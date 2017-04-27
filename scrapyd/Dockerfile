FROM bossjones/boss-docker-python3

ADD requirements.txt /home/

WORKDIR /home/

RUN pip install --upgrade pip && \
    pip install -r /home/requirements.txt

EXPOSE 6800

CMD ["scrapyd"]