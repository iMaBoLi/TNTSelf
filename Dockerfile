FROM python:3.10

ENV TZ=Asia/Tehran
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . /app/
WORKDIR /app/

RUN apt-get update
RUN apt-get install -y ffmpeg

RUN pip3 install -U pip
RUN pip3 install -q --no-cache-dir -r requirements.txt
RUN pip3 install -q --no-cache-dir -r other-requirements.txt

CMD ["python3", "-m", "FidoSelf"]
