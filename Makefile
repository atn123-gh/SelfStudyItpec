.PHONY: up down restart logs build ps restore-mongo shell-db shell-mongo

# Starts the app, Postgres, and MongoDB. nginx/certbot are intentionally
# excluded — not needed for this project's HTTP-only, no-domain setup.
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

# One-time (or repeat any time you want to reset back to real data):
# restores real MongoDB solution content over the dummy placeholder data.
restore-mongo:
	./scripts/restore-mongo.sh

shell-db:
	docker compose exec db psql -U itp_user -d itpdb

shell-mongo:
	docker compose exec mongodb mongosh -u root -p example --authenticationDatabase admin
