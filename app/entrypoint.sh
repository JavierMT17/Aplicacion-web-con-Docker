#!/bin/sh
set -e

mkdir -p certs
if [ ! -f certs/server.key ] || [ ! -f certs/server.crt ]; then
  openssl req -x509 -newkey rsa:4096 -days 365 -nodes \
    -subj "/C=ES/ST=Madrid/L=Madrid/O=Aplicacion Docker/OU=Dev/CN=localhost" \
    -keyout certs/server.key -out certs/server.crt
fi

python app.py
