# Development & Deployment Guide

Technical reference for running, developing, and deploying this project.
For a general overview of what this project is, see [README.md](README.md).

## Quick Start (Docker Compose)

This is the current, supported way to run this project — locally or on any
fresh machine (e.g. a new DigitalOcean droplet). It's Docker Compose end to
end: no native Python/Postgres/Mongo install needed on the host, and the
same `docker-compose.yml` works unmodified in every environment.

### Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine + the Compose plugin (Linux)
- That's it — Postgres, MongoDB, and the app itself all run in containers.

### One-time setup

1. Copy `.env.example` to `.env` and fill in real values (see the comments
   in that file for what each variable means and which ones are safe to
   leave as-is vs. must be generated fresh). **Never commit `.env`.**
2. `make build` (or `docker compose up --build -d app db mongodb`) — builds
   the app image, starts Postgres + MongoDB + the app, runs migrations, and
   seeds Postgres with real quiz metadata automatically.
3. `make restore-mongo` (or `./scripts/restore-mongo.sh`) — one-time step
   to load real MongoDB solution content from `mongo_data_bk/`, replacing
   the dummy placeholder text the app seeds by default (see "Known quirks"
   below for why this extra step exists).
4. Open the app at `http://localhost:8000/home/` (or whatever
   `APP_HOST_PORT` you set in `.env`). For a public deployment reachable
   over HTTPS at `https://<your-server-ip>`, see "HTTPS via public IP"
   below instead of step 4.

### Everyday commands

| Command | What it does |
|---|---|
| `make up` | Start app + db + mongodb (no rebuild) |
| `make down` | Stop and remove all containers |
| `make restart` | Restart app + db + mongodb |
| `make logs` | Follow the app container's logs |
| `make build` | Rebuild the app image and start everything |
| `make ps` | Show container status |
| `make restore-mongo` | Re-load real MongoDB data (see above) |
| `make shell-db` | Open a `psql` shell into Postgres |
| `make shell-mongo` | Open a `mongosh` shell into MongoDB |
| `make init-https` | One-time: bootstrap the HTTPS deployment (see below) |
| `make up-https` | Start the full stack including nginx/certbot (after `init-https`) |
| `make logs-nginx` / `make logs-certbot` | Follow those containers' logs |

No `make`? Run the equivalent `docker compose ...` command shown in the
`Makefile` — it's a one-line wrapper for each target.

### HTTPS via public IP (no domain)

For a deployment reachable at `https://<your-server-ip>` — a real,
publicly-trusted certificate, not self-signed — using Let's Encrypt's
IP-address certificate support (GA since January 2026). No domain name
needed.

**How it works:** nginx terminates TLS and reverse-proxies to the app
container (which is otherwise only reachable from `localhost` — see
`docker-compose.yml`). Certbot obtains the certificate via HTTP-01
validation (nginx serves the challenge on port 80) using the
`shortlived` ACME profile — the only profile currently available for
bare IP addresses. These certificates are valid for **~160 hours (~6.7
days)**, not the usual 90 days, so a renewal loop (built into the
`certbot` service, checking every 6h) is essential, not optional.

1. In `.env`, set `SERVER_IP` (your server's public IP) and
   `LETSENCRYPT_EMAIL` (used only for renewal-failure notices) — see
   `.env.example`.
2. `make build` first if you haven't already (builds the app image,
   starts app/db/mongodb).
3. `make init-https` — one-time bootstrap: creates a temporary
   self-signed cert so nginx can start, brings up nginx, requests the
   real certificate, reloads nginx, and starts the renewal loop. Takes
   under a minute. Safe to re-run if something fails partway.
4. Open `https://<SERVER_IP>`.

After the first run, `make up-https` (or just `make up` — nginx/certbot
keep running once started with `restart: unless-stopped`) is all you
need for ordinary restarts. Firewall: open 22 (SSH), 80 (HTTP — needed
for renewal, not just redirects), and 443 (HTTPS); nothing else.

**Why the certificate needs an automated renewal loop, and what happens
if it lapses:** unlike a normal 90-day certificate where a missed
renewal check has weeks of slack, a ~160-hour cert lapsing means the
site starts serving an expired certificate (browsers will show a
warning, not silently fall back to HTTP) within days of the renewal
loop stopping. As long as the `certbot` container keeps running
(`docker compose ps` to check), this is handled automatically — there's
nothing to do manually.

### Deploying to a new machine

1. Copy the repo to the machine (any method — `scp`, `rsync`, a zip file;
   this repo isn't currently a git repository).
2. Install Docker + the Compose plugin if not already present.
3. Copy `.env.example` to `.env`, fill in real values for *that* machine —
   in particular:
   - `DJANGO_SECRET_KEY`: generate a fresh one (see `.env.example`)
   - `DJANGO_ALLOWED_HOSTS`: add that machine's IP or hostname
   - `POSTGRES_PASSWORD`: choose a real password (the placeholder in
     `.env.example` is not safe to use as-is)
   - For HTTPS (recommended): also set `SERVER_IP` and `LETSENCRYPT_EMAIL`
     — see "HTTPS via public IP" above
4. `make build`, then `make restore-mongo` once.
5. `make init-https` for HTTPS (see above), or just `make up` for
   plain HTTP on `APP_HOST_PORT` (bound to localhost only by default —
   see the comment in `docker-compose.yml` if you specifically want
   unencrypted HTTP reachable from outside instead of HTTPS).
6. Open a firewall for SSH (22) and either 80+443 (HTTPS) or your chosen
   `APP_HOST_PORT` (plain HTTP) — nothing else needs to be public.
   MongoDB's port is bound to `127.0.0.1` in `docker-compose.yml`, so
   it's never exposed regardless.

### Known quirks (so you don't have to rediscover them)

- `entrypoint.sh` force-sets `DJANGO_DEBUG=True` at container startup
  regardless of `.env`, which means the app always runs via Django's
  `runserver` (not gunicorn) under `settings/local.py` (not
  `settings/production.py`), every environment, every time. This is
  intentional for this project's "not production-grade, keep it simple"
  goal — gunicorn/`production.py` are installed/present but unused. If you
  ever want a hardened gunicorn+production setup, that's a separate, scoped
  change (fix the missing MongoDB config in `production.py`, relax its
  HTTPS-only cookie settings, remove the `entrypoint.sh` override) — not
  needed for local dev or a demo deployment.
- `entrypoint.sh` runs `init_noSql` on every container start, which seeds
  MongoDB with **dummy placeholder text** ("dummy Q1 solution", etc.) if
  the collections don't already have data. Run `make restore-mongo` after
  bringing the stack up to replace it with the real content from
  `mongo_data_bk/`.
- `init-letsencrypt.sh` and `nginx/production.conf` are leftover from the
  *original* HTTPS + custom-domain deployment (a real domain, standard
  90-day certs) — **not used** now. The current HTTPS setup
  (`nginx/templates/ip-https.conf.template`, `scripts/init-https.sh`) is
  a different, IP-address-based approach with short-lived certificates —
  see "HTTPS via public IP" above. `nginx/localhost.conf` is also unused
  (a leftover from that original setup) since nginx isn't part of the
  plain-HTTP local dev flow at all.
- `make up` / `make build` only start `app db mongodb` — nginx/certbot
  only start via `make up-https` / `make init-https`.

---

## Legacy notes (from the original deployment — kept for reference)

The sections below describe the *original* HTTPS + custom-domain deployment
process this project used. They're **not** part of the current workflow
(see "Quick Start" above) but are kept here since some of the raw commands
are still useful for troubleshooting.

#### Generate Secret Key
```
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
```

#### Know-How for DO Droplets (original HTTPS+domain flow — not current)
1. Install git, docker, docker-compose
2. `git pull`
3. `init-letsencrypt.sh` (only first time) — not used in the current setup
4. `docker-compose up`
5. Buy domain name, DNS redirect, add allowed hosts — not used in the
   current IP-only setup

#### Switching nginx configs (original flow — not current)
Comment out whichever of `nginx/localhost.conf` / `nginx/production.conf`
isn't in use. Not applicable now since nginx isn't part of the current
setup at all.

#### Useful raw commands

[Postgres Issue #203](https://github.com/docker-library/postgres/issues/203)

Remove all volumes:
```bash
docker volume ls | awk '$1 == "local" { print $2 }' | xargs --no-run-if-empty docker volume rm
```

Remove all containers:
```bash
docker rm $(docker ps -aq)
```

Execute SQL command in Docker:
```bash
docker exec -it selfstudyitpec-db-1 psql -U itp_user -d itpdb -c "SELECT * FROM home_feedback"
```

Connect to MongoDB shell:
```bash
docker exec -it selfstudyitpec-mongodb-1 mongosh -u root -p example --authenticationDatabase admin
```
```
use mongo_db
db.ip_questions.find().pretty()
db.fe_questions.find().pretty()
```

Re-create the MongoDB backup used by `scripts/restore-mongo.sh`:
```bash
docker exec selfstudyitpec-mongodb-1 mongodump -u root -p example --authenticationDatabase admin --db mongo_db --out /mongo_data_bk
docker cp selfstudyitpec-mongodb-1:/mongo_data_bk ./mongo_data_bk
```

For logging, use Sentry instead of manual logging (already wired into
`settings/base.py`).
