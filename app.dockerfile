FROM python:3.9-slim-buster
WORKDIR /app
RUN apt-get update && apt install curl -y && apt-get install -y python3-opencv
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY backend/src/ backend/src/
COPY run_app_production.sh run.sh
ENTRYPOINT ["/bin/sh", "./run.sh"]