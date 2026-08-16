#!/bin/bash

# Directory where backups are stored
backup_dir="./backup/"

#!/bin/bash

# Directory where backups are stored
backup_dir="./backup/"

# Ensure the backup directory exists
mkdir -p "$backup_dir"

db_user="itp_user"
db_name="itpdb"

# Create a timestamp
timestamp=$(date +"%Y%m%d_%H%M%S")

# Dump all tables from the PostgreSQL database as SQL insert statements
pg_dump -U $db_user -d $db_name --data-only --inserts --file="${backup_dir}db_backup_$timestamp.sql"
echo "Backup dump completed as SQL insert statements"


# Export all tables in the database as SQL INSERT statements into the same file
backup_file="${backup_dir}db_backup_$timestamp.sql"
psql -U $db_user -d $db_name -t -c \
"SELECT tablename FROM pg_tables WHERE schemaname = 'public';" | while read -r table_name; do
    if [[ -n "$table_name" ]]; then
        echo "Exporting table: $table_name"
        echo "-- Exporting table: $table_name" >> "$backup_file"
        pg_dump -U $db_user -d $db_name --data-only --inserts --table="$table_name" >> "$backup_file"
        echo "" >> "$backup_file" # Add a newline between tables
    fi
done

echo "All tables export completed"



