#!/bin/bash
# One-time bootstrap for the HTTPS-via-public-IP deployment:
#   1. Creates a temporary self-signed cert so nginx can start at all
#      (it refuses to start with `ssl_certificate` pointing at a file
#      that doesn't exist yet).
#   2. Brings up the stack.
#   3. Requests a REAL Let's Encrypt IP-address certificate - these use
#      the "shortlived" ACME profile (~160h / ~6.7 day validity; that's
#      the only profile currently available for bare IP addresses, see
#      README), validated over plain HTTP (http-01) since there's no
#      domain to validate via DNS.
#   4. Reloads nginx to pick up the real certificate.
#   5. Starts the certbot renewal loop (checks every 6h - see
#      docker-compose.yml).
#
# Re-running this script is safe (idempotent) - e.g. if the first
# certonly attempt fails, fix the issue and just run it again.
#
# Usage: ./scripts/init-https.sh
set -euo pipefail
cd "$(dirname "$0")/.."
export MSYS_NO_PATHCONV=1

SERVER_IP="$(grep -m1 '^SERVER_IP=' .env | cut -d= -f2-)"
LE_EMAIL="$(grep -m1 '^LETSENCRYPT_EMAIL=' .env | cut -d= -f2-)"

if [ -z "$SERVER_IP" ]; then
  echo "SERVER_IP is not set in .env (your droplet's public IP) - add it and re-run." >&2
  exit 1
fi
if [ -z "$LE_EMAIL" ]; then
  echo "LETSENCRYPT_EMAIL is not set in .env - add it and re-run." >&2
  exit 1
fi

CERT_DIR="./data/certbot/conf/live/$SERVER_IP"

echo "== [1/5] Creating a temporary self-signed certificate =="
mkdir -p "$CERT_DIR"
openssl req -x509 -nodes -newkey rsa:2048 -days 1 \
  -keyout "$CERT_DIR/privkey.pem" \
  -out "$CERT_DIR/fullchain.pem" \
  -subj "/CN=$SERVER_IP"

echo "== [2/5] Starting app, db, mongodb, nginx =="
docker compose up -d app db mongodb nginx

echo "== [3/5] Removing the temporary certificate =="
rm -rf ./data/certbot/conf/live ./data/certbot/conf/archive ./data/certbot/conf/renewal
mkdir -p "$CERT_DIR"

echo "== [4/5] Requesting a real Let's Encrypt IP-address certificate =="
docker compose run --rm --entrypoint certbot certbot certonly \
  --webroot --webroot-path /var/www/certbot \
  --preferred-profile shortlived \
  --ip-address "$SERVER_IP" \
  --non-interactive --agree-tos \
  -m "$LE_EMAIL"

echo "== [5/5] Reloading nginx and starting the renewal loop =="
docker compose exec nginx nginx -s reload
docker compose up -d certbot

echo ""
echo "Done. Site should be reachable at https://$SERVER_IP"
echo "Note: this certificate is valid for ~6.7 days. The certbot service"
echo "now runs a renewal check every 6h automatically - no further action"
echo "needed as long as the certbot container keeps running."
