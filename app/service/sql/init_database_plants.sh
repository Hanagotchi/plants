#!/bin/bash

set -e
set -u

echo "  Creating user and database '$PLANTS_DB' "
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
	CREATE DATABASE "$PLANTS_DB";
	GRANT ALL PRIVILEGES ON DATABASE "$PLANTS_DB" TO "$POSTGRES_USER";
EOSQL