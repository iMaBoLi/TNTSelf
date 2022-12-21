FROM python:3.10

COPY . /root/
WORKDIR /root/

RUN pip3 install -U pip
RUN pip3 install -q yt-dlp
RUN pip3 install -q speedtest-cli
RUN pip3 install -U -r requirements.txt

CMD ["python3", "-m", "FidoSelf"]
