FROM python:3.8

WORKDIR  /EfreiBot

ADD . /EfreiBot

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD [ "python", "app.py"]