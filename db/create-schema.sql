CREATE TABLE IF NOT EXISTS token (
    "address" bytea NOT NULL PRIMARY KEY,
    "symbol" varchar(5) NOT NULL UNIQUE,
    "name" varchar(32) NOT NULL,
    "decimals" int2 NOT NULL,
    "total_supply" float8 NOT NULL
);


CREATE TABLE IF NOT EXISTS token_transfer (
    "id" SERIAL PRIMARY KEY,
    "token_address" bytea NOT NULL REFERENCES token("address") ON DELETE CASCADE,
    "from_address" bytea NOT NULL,
    "to_address" bytea NOT NULL,
    "value" float8 NOT NULL,
    "transaction_hash" bytea NOT NULL,
    "log_index" int8 NOT NULL,
    "block_timestamp" timestamp NOT NULL,
    "block_number" int8 NOT NULL,
    "block_hash" bytea NOT NULL
);


GRANT ALL PRIVILEGES ON TABLE token TO terminal_user;
GRANT ALL PRIVILEGES ON TABLE token_transfer TO terminal_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO terminal_user;
