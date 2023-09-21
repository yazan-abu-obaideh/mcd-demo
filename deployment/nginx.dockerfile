FROM nginx

COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/secrets/ /secrets/
COPY frontend/src/decode.html /static/decode.html
COPY frontend/src/read-more.html /static/read-more.html
COPY frontend/src/styles.css /static/styles.css
COPY frontend/src/assets/ /static/assets/
COPY frontend/src/js/target/client.js /static/js/target/client.js
