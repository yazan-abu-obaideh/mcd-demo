FROM nginx

COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/secrets/ /secrets/
COPY frontend/web/dist/ /static/
