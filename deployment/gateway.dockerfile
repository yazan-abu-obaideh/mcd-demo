FROM nginx

COPY nginx/gateway_nginx.conf /etc/nginx/nginx.conf
COPY nginx/secrets/ /secrets/
