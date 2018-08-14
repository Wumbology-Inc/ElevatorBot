FROM python:3.6-alpine

RUN apk update && apk upgrade 
RUN apk add --no-cache git ffmpeg bash opus

# Add build files for PyNaCl
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev

RUN set -ex && mkdir /app
WORKDIR /app
ADD . /app

COPY requirements.txt requirements.txt
RUN set -ex && pip install --verbose -r requirements.txt

RUN apk del .pynacl_deps

COPY credentials.JSON credentials.JSON
CMD ["python", "elevatorbotLogin.py"]