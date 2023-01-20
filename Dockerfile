FROM python:3.10

COPY . /app/
WORKDIR /app/

EXPOSE 3000 35729

RUN apt-get update
RUN apt-get install -y ffmpeg

RUN pip3 install -U pip
RUN pip3 install -U -r requirements.txt
RUN pip3 install -U -r other-requirements.txt

CMD ["python3", "-m", "FidoSelf]
