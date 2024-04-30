#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "postgres" <<-EOSQL
	CREATE USER appuser WITH PASSWORD 'devpassword';
	CREATE DATABASE devdb WITH owner appuser;
	GRANT ALL PRIVILEGES ON DATABASE devdb TO appuser;
EOSQL

psql -U postgres -d devdb <<-EOSQL
  CREATE extension vector;
EOSQL

