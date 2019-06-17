DROP TABLE IF EXISTS token_transfer_temp_ID;

CREATE TABLE token_transfer_temp_ID (
    "id" SERIAL PRIMARY KEY,
    "token_address" bytea NOT NULL,
    "from_address" bytea NOT NULL,
    "to_address" bytea NOT NULL,
    "value" float8 NOT NULL,
    "transaction_hash" bytea NOT NULL,
    "log_index" int8 NOT NULL,
    "block_timestamp" timestamp NOT NULL,
    "block_number" int8 NOT NULL,
    "block_hash" bytea NOT NULL
);


GRANT ALL PRIVILEGES ON TABLE token_transfer_temp_ID TO terminal_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO terminal_user;
