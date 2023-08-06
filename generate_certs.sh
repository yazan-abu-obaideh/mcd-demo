mkdir nginx/secrets -p
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx/secrets/nginx-selfsigned.key -out nginx/secrets/nginx-selfsigned.crt
#sudo openssl dhparam -out dhparam.pem 4096