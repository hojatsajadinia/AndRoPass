FROM python:3.11-alpine

RUN apk update
RUN apk add \
    bash \
    wget \
    tar \
    gzip \
    ca-certificates \
    openjdk17-jdk

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "AndRoPass.py"]
