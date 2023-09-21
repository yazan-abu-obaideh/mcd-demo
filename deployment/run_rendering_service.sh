Xvfb :99 -screen 0 800x600x8 &
export DISPLAY=:99
cd ${APP_ROOT_DIR}
gunicorn -w ${APP_WORKERS} -b ${APP_HOSTNAME}:${APP_PORT} --threads ${APP_THREADS} "app:build_rendering_app()"