FROM ubuntu:latest
COPY dist/ dist/
RUN apt-get update && apt install default-jre -y
ENTRYPOINT dist/optimization_app_dev/optimization_app_dev
