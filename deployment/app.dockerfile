FROM python:3.9-slim-buster
WORKDIR /app

RUN apt-get update && apt install curl python3-opencv openjdk-11-jre xvfb -y
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY backend/src/ backend/src/
COPY backend/MANIFEST.in backend/MANIFEST.in
COPY backend/pyproject.toml backend/pyproject.toml
RUN pip install ./backend

COPY deployment/run_optimization_service.sh run_optimization_service.sh
COPY deployment/run_rendering_service.sh run_rendering_service.sh
