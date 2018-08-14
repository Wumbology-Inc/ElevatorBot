FROM python:3.6-alpine
# Add git
RUN apk update && apk upgrade 
RUN apk add --no-cache git
RUN apk add --no-cache ffmpeg

RUN set -ex && mkdir /app

WORKDIR /app
ADD . /app

COPY requirements.txt requirements.txt
RUN set -ex && pip install -r requirements.txt

COPY credentials.JSON credentials.JSON
CMD ["python", "elevatorbotLogin.py"]