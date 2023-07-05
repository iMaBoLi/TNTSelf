FROM python:3

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
  echo "deb http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google.list && \
  apt-get update -y && \
  apt-get install -y google-chrome-stable xvfb libxi6 libgconf-2-4 default-jdk && \
  chmod +x /usr/bin/google-chrome
RUN yay -S google-chrome
RUN dnf install https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
RUN apt-get install -y chromium-browser

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "bash", "start.sh"]