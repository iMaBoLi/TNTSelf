FROM python:3

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

COPY . .

RUN apt-get update
RUN apt-get install -y ffmpeg

RUN pip3 install -U pip
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "-m", "FidoSelf"]