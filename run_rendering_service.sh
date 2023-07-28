Xvfb :99 -screen 0 800x600x8 &
export DISPLAY=:99
gunicorn -w ${APP_WORKERS} -b ${APP_HOSTNAME}:${APP_PORT} "app:app"