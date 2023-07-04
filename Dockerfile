FROM python:3

RUN pip install --upgrade pip

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y ffmpeg

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME ["/usr/src/app"]

CMD [ "python3", "-m", "FidoSelf", "runserver", "0:8000" ]