FROM python:3

RUN pip install -U pip

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y ffmpeg

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

VOLUME ["/usr/src/app"]

CMD [ "bash", "start.sh", "runserver", "0:8000"]