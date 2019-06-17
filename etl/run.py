from etl import performEtl
import load
import transform

tokenConfig = {
    # common
    'id': 0,
    'number_of_instances': 1,

    # extract
    'extractUrl': 'https://storage.googleapis.com/terminal-public-buckets/assignment-data/tokens/tokens',

    # transform
    'types': {
        'address': 'bytes',
        'decimals': 'uint8',
        'total_supply': 'float64'
    },
    'transform': transform.transformTokens,
    'transformHandler': transform.transformTokensHandler,

    # load
    'load': load.loadTokens,
    'connectionString': 'postgresql://terminal_user:terminal_pass@localhost:5432/terminal'
}
performEtl(tokenConfig)


tokenTransferConfig = {
    # common
    'id': 0,
    'number_of_instances': 1,

    # extract
    'extractUrl': 'https://storage.googleapis.com/terminal-public-buckets/assignment-data/token-transfers/token-transfer',

    # transform
    'types': {
        'token_address': 'bytes',
        'from_address': 'bytes',
        'to_address': 'bytes',
        'value': 'float64',
        'transaction_hash': 'bytes',
        'log_index': 'uint64',
        'block_number': 'uint64',
        'block_hash': 'bytes'
    },
    'transform': transform.transformTokenTransfers,
    'transformHandler': transform.transformTokenTransfersHandler,

    # load
    'load': load.loadTokenTransfers,
    'connectionString': 'postgresql://terminal_user:terminal_pass@localhost:5432/terminal'
}
performEtl(tokenTransferConfig)
