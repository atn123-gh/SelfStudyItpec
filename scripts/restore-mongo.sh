#!/bin/bash
# Restores the real quiz-solution data into MongoDB, replacing the
# placeholder/dummy text ("dummy Q1 solution", etc.) that entrypoint.sh's
# init_noSql management command auto-seeds on every container start.
#
# Run this once after `make up` (or docker compose up) on any machine —
# local or a fresh deployment — to get real solution content.
#
# Usage: ./scripts/restore-mongo.sh
set -euo pipefail
cd "$(dirname "$0")/.."

# On Windows Git Bash (MSYS), absolute-looking paths passed as command
# arguments get silently rewritten to a Windows path before reaching
# `docker`, which breaks the in-container path below. This disables that
# rewriting; it's a no-op on Linux/macOS.
export MSYS_NO_PATHCONV=1

# Read directly from .env (targeted extraction, not a full `source`, so
# special characters in the password can't be interpreted as shell syntax).
MONGO_USER="$(grep -m1 '^MONGO_DB_USERNAME=' .env | cut -d= -f2-)"
MONGO_PASS="$(grep -m1 '^MONGO_DB_PASSWORD=' .env | cut -d= -f2-)"

docker compose exec mongodb mongorestore \
  --username "$MONGO_USER" \
  --password "$MONGO_PASS" \
  --authenticationDatabase admin \
  --drop \
  /mongo_data_bk

echo "MongoDB restored from mongo_data_bk/ (dummy placeholder data replaced with real content)."
