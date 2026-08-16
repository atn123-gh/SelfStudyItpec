.PHONY: up down restart logs build ps restore-mongo shell-db shell-mongo up-https init-https logs-nginx logs-certbot

# Starts the app, Postgres, and MongoDB. nginx/certbot are intentionally
# excluded — only needed for the HTTPS deployment (see up-https below).
up:
	docker compose up -d app db mongodb

down:
	docker compose down

restart:
	docker compose restart app db mongodb

logs:
	docker compose logs -f app

# Rebuilds the app image (needed after changing requirements/ or the
# Dockerfile) and starts everything.
build:
	docker compose up --build -d app db mongodb

ps:
	docker compose ps

# HTTPS-via-public-IP deployment. First time on a machine: use
# `init-https` instead (handles the initial certificate). After that,
# `up-https` is what you'd use for ordinary restarts.
up-https:
	docker compose up -d app db mongodb nginx certbot

# One-time (per machine): bootstraps a real Let's Encrypt IP-address
# certificate and starts the full HTTPS stack. Requires SERVER_IP and
# LETSENCRYPT_EMAIL set in .env — see .env.example.
init-https:
	./scripts/init-https.sh

logs-nginx:
	docker compose logs -f nginx

logs-certbot:
	docker compose logs -f certbot

# One-time (or repeat any time you want to reset back to real data):
# restores real MongoDB solution content over the dummy placeholder data.
restore-mongo:
	./scripts/restore-mongo.sh

shell-db:
	docker compose exec db psql -U itp_user -d itpdb

shell-mongo:
	docker compose exec mongodb mongosh -u root -p example --authenticationDatabase admin
