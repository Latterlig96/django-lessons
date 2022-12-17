psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
    CREATE DATABASE django;
    GRANT ALL PRIVILEGES ON DATABASE django TO postgres;
EOSQL
echo "Created database django for user postgres";