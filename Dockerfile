FROM python:3.10

COPY . /app/
WORKDIR /app/

ENV TZ=Asia/Tehran
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN bash installer.sh

CMD ["bash", "startup"]
