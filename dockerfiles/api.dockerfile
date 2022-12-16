FROM python:3.10

COPY . /central
WORKDIR /central

RUN pip install -r requirements.txt

# CMD [ "sh", "-c", "python", "main.py" ]
