db-1       | initdb: error: directory "/var/lib/postgresql/data" exists but is not empty
db-1       | initdb: hint: If you want to create a new database system, either remove or empty the directory "/var/lib/postgresql/data" or run initdb with an arg
      - postgres_data:/var/lib/postgresql/data/

Tmp workaround:
   -stop docker, rmove all volume
   -start docker comment out all postgres_data volume
   remove comment for "entrypoint: ["/bin/sh", "-c", "rm -rf /var/lib/postgresql/data/*; docker-entrypoint.sh postgres"]" to delete the folder.( comment out again  after ward)