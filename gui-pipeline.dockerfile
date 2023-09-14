FROM ubuntu:latest
COPY dist/ dist/
ENTRYPOINT dist/optimization_app_dev/optimization_app_dev
