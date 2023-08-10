mkdir nginx/secrets -p
cp /etc/letsencrypt/live/mcd-demo.com/fullchain.pem nginx/secrets/fullchain.pem
cp /etc/letsencrypt/live/mcd-demo.com/privkey.pem nginx/secrets/privkey.pem
#sudo openssl dhparam -out dhparam.pem 4096