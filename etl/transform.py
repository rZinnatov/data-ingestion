import pandas as pd
from transform_helper import transform, transformHash, transformRegex, transformString


def transformTokens(df, config):
    df = transform(df, config.handler, config.types)
    df.dropna(inplace=True)
    df.drop_duplicates('address', inplace=True)
    df.drop_duplicates('symbol', inplace=True)

    return df


def transformTokensHandler(row):
    return pd.Series([
        transformHash(row['address']),
        transformString(row['symbol'], 1, 5, '[^A-Z]'),
        transformString(row['name'], 1, 32, '[^\w \._-]'),
        row['decimals'],
        row['total_supply']
    ])


def transformTokenTransfers(df, config):
    df = transform(df, config.handler, config.types)
    df.dropna(inplace=True)

    return df


def transformTokenTransfersHandler(row):
    return pd.Series([
        transformHash(row['token_address']),
        transformHash(row['from_address']),
        transformHash(row['to_address']),
        row['value'],
        transformHash(row['transaction_hash']),
        row['log_index'],
        transformRegex(row['block_timestamp'], '[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) (2[0-3]|[01][0-9]):[0-5][0-9]:[0-5][0-9] UTC'),
        row['block_number'],
        transformHash(row['block_hash'])
    ])
