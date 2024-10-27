import numpy as np
import pandas as pd
import math

import stumpy
from stumpy import config


def compute_mp(ts1: np.ndarray, m: int, exclusion_zone: int = None, ts2: np.ndarray = None):
    """
    Compute the matrix profile

    Parameters
    ----------
    ts1: the first time series
    m: the subsequence length
    exclusion_zone: exclusion zone
    ts2: the second time series

    Returns
    -------
    output: the matrix profile structure
            (matrix profile, matrix profile index, subsequence length, exclusion zone, the first and second time series)
    """

    mp={}
    # Преобразуем входные данные к np.ndarray, если требуется
    if isinstance(ts1, np.ndarray):
        ts1 = np.array(ts1).astype(np.float64)
        mp = stumpy.stump(ts1, m)
    if isinstance(ts2, np.ndarray):
        ts2 = np.array(ts2).astype(np.float64)
        mp = stumpy.stump(ts1, m, T_B=ts2)

    print(mp)
    return {'mp': mp[:, 0],
            'mpi': mp[:, 1],
            'm' : m,
            'excl_zone': exclusion_zone,
            'data': {'ts1' : ts1, 'ts2' : ts2}
            }
