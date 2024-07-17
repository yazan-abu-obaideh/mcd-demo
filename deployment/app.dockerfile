FROM python:3.9.19-slim
WORKDIR /app

RUN apt-get update && apt install curl python3-opencv default-jre xvfb -y
COPY requirements-lock.txt requirements-lock.txt
RUN pip install --no-cache-dir -r requirements-lock.txt

COPY backend/src/ backend/src/
COPY backend/MANIFEST.in backend/MANIFEST.in
COPY backend/pyproject.toml backend/pyproject.toml
RUN pip install ./backend

COPY deployment/run_optimization_service.sh run_optimization_service.sh
COPY deployment/run_rendering_service.sh run_rendering_service.sh
