mkdir nginx/secrets -p
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx/secrets/nginx-selfsigned.key -out nginx/secrets/nginx-selfsigned.crt
export CERTDATA=$(sudo cat nginx/secrets/nginx-selfsigned.key)
rm -f nginx/secrets/nginx-selfsigned.key
echo $CERTDATA > nginx/secrets/nginx-selfsigned.key
