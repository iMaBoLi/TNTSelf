FROM python:3.11

RUN apt-get update
RUN apt-get upgrade
RUN apt-get install -y ffmpeg

COPY . /app/
WORKDIR /app/

RUN pip3 install -U pip
RUN pip3 install -U -r requirements.txt

CMD ["python3", "-m", "FidoSelf"]
