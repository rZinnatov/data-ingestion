from sqlalchemy import create_engine


def loadTokens(df, config):
    df.to_sql('token', engine, if_exists='append', index=False)


def loadTokenTransfers(df, config):
    engine = create_engine(config.connectionString)

    df.to_sql(f'token_transfer_temp_{config.id}', engine, if_exists='append', index=False)

    # HACK:
    # pandas/sqlalchemy send bulk inserts
    # there is relation: TokenTransfer.token_address == Token.address
    # some tokens were invalid and didn't go to storage
    # hence some inserts will fail, failed records should be ignored
    # so, a nasty workaround to keep things simple
    with engine.begin() as context:
        context.execute(f'INSERT INTO token_transfer (SELECT * FROM token_transfer_temp_{config.id} t WHERE t.token_address IN (SELECT address from token));')
        context.execute(f'DELETE FROM token_transfer_temp_{config.id};')
