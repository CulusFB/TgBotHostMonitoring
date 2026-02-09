FROM --platform=$TARGETPLATFORM  python:3.14-alpine

LABEL authors="CulusFB"

WORKDIR /hostMonitor
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .


CMD ["python", "main.py"]
