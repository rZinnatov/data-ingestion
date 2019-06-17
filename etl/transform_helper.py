import re
import numpy as np
import pandas as pd
from multiprocessing import cpu_count, Pool


def transform(df, handler, types={}):
    transformed_df = _parallel_apply(
        df,
        handler,
        axis=1,
        workers=cpu_count()
    )

    transformed_df.columns = df.columns
    transformed_df = transformed_df.dropna()
    for column, to_type in types.items():
        transformed_df[column] = transformed_df[column].astype(to_type)

    return transformed_df


def _apply_df(args):
    df, func, kwargs = args
    return df.apply(func, **kwargs)


def _parallel_apply(df, func, **kwargs):
    workers = kwargs.pop('workers')
    pool = Pool(processes=workers)
    result = pool.map(_apply_df, [(d, func, kwargs) for d in np.array_split(df, workers)])
    pool.close()
    pool.join()
    return pd.concat(list(result))


def transformHash(hash):
    try:
        return bytes.fromhex(hash[2:])
    except ValueError as ex:
        # TODO: Log erroneous hash
        return np.nan


def transformRegex(value, regex):
    value_str = str(value)

    if not re.search(regex, value_str):
        # TODO: Log erroneous value
        return np.nan

    return value


def transformString(value, min_len, max_len, regex):
    value_str = str(value)

    value_length = len(value_str)
    if value_length < min_len or max_len < value_length:
        # TODO: Log erroneous value
        return np.nan

    value_stripped = value_str.strip('\'" \t')
    if re.search(regex, value_stripped):
        # TODO: Log erroneous value
        return np.nan

    return value_stripped
