FROM python:3

COPY . /app/
WORKDIR /app/

RUN apt-get update
RUN apt-get install -y ffmpeg

RUN pip3 install -U pip
RUN pip3 install -r --no-cache-dir requirements.txt

CMD ["python3", "-m", "FidoSelf"]
