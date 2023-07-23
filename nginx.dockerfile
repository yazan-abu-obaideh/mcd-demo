FROM nginx

COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/secrets/nginx-selfsigned.crt /secrets/nginx-selfsigned.crt
COPY nginx/secrets/nginx-selfsigned.key /secrets/nginx-selfsigned.key
COPY frontend/src/decode.html /static/decode.html
COPY frontend/src/styles.css /static/styles.css
COPY frontend/src/assets/ /static/assets/
COPY frontend/src/js/target/client.js /static/js/target/client.js
