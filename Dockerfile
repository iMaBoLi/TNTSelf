FROM python:3.11.2

COPY . /app/
WORKDIR /app/

RUN apt-get update
RUN apt-get install -y ffmpeg

RUN pip3 install -U pip
RUN pip3 install -U -r requirements.txt
RUN pip3 install git+https://github.com/alexmercerind/youtube-search-python
RUN pip3 install git+https://github.com/yt-dlp/yt-dlp

CMD ["python3", "-m", "FidoSelf"]