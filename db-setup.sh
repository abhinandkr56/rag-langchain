# define the environment variables
# POSTGRES_VERSION=15.6

POSTGRES_VERSION=16.2 # the version of PostgreSQL
POSTGRES_USER=postgres  # the default super admin of the database instance. Change this if you want a different user
POSTGRES_PASSWORD=devpassword # change the password to your favorite password
POSTGRES_CONTAINER=postgres-langchain-dev # friendly name for the postgres container
POSTGRES_DB=postgres
DEVDB_NAME=devdb


# create db script


cat << EOF > init-user-db.sh
#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER appuser WITH PASSWORD 'devpassword';
	CREATE DATABASE ${DEVDB_NAME} WITH owner appuser;
	GRANT ALL PRIVILEGES ON DATABASE devdb TO appuser;
EOSQL

psql -U ${POSTGRES_USER} -d ${DEVDB_NAME} <<-EOSQL
  CREATE extension vector;
EOSQL

EOF

# set the permissions
chmod +x init-user-db.sh

# pull the required image
docker pull postgres:${POSTGRES_VERSION}
# https://github.com/pgvector/pgvector?tab=readme-ov-file#docker
docker pull pgvector/pgvector:pg16

export POSTGRES_IMAGE=postgres:${POSTGRES_VERSION}
# use the image with pgvector pre installed
export POSTGRES_IMAGE=pgvector/pgvector:pg16

# create the postgres container
docker run --name ${POSTGRES_CONTAINER} \
  -e POSTGRES_USER=${POSTGRES_USER} -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} -p 5433:5432 \
  -v ./init-user-db.sh:/docker-entrypoint-initdb.d/init-user-db.sh \
  --restart unless-stopped \
  -d ${POSTGRES_IMAGE} 

docker exec -it ${POSTGRES_CONTAINER} bash


docker stop ${POSTGRES_CONTAINER}
#docker rm ${POSTGRES_CONTAINER}