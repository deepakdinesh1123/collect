FROM python:3.10

COPY . /central
WORKDIR /central

RUN pip install -r requirements.txt

# ENTRYPOINT [ "/bin/bash -c", "rq", "worker", "--url", "redis://$REDIS_HOST:6379" ]

CMD [ "sh", "-c", "rq worker -c rq_config" ]
