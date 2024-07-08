FROM python:3.10.4-slim-buster
RUN apt-get update && apt -y install git curl wget python3-pip bash neofetch ffmpeg software-properties-common
COPY requirements.txt .

RUN pip3 install wheel
RUN pip3 install --no-cache-dir -U -r requirements.txt
WORKDIR /app
COPY . .

CMD flask run -h 0.0.0.0 -p 8000 & python3 -m devgagan
