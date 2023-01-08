FROM python:3.10

COPY . /app/
WORKDIR /app/

RUN apt-get update
RUN apt-get install -y ffmpeg

RUN pip install --upgrade pip
RUN pip3 install -q --no-cache-dir -r requirements.txt

CMD ["python3", "-m", "FidoSelf"]
