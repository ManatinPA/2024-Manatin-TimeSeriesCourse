import numpy as np

from modules.utils import z_normalize
from modules.metrics import ED_distance, norm_ED_distance


def brute_force(ts: np.ndarray, query: np.ndarray, is_normalize: bool = True) -> np.ndarray:
    """
    Calculate the distance profile using the brute force algorithm

    Parameters
    ----------
    ts: time series
    query: query, shorter than time series
    is_normalize: normalize or not time series and query

    Returns
    -------
    dist_profile: distance profile between query and time series
    """

    n = len(ts)
    m = len(query)
    N = n-m+1
    
    dist_profile = np.zeros(shape=(N,))
    _query=None
    if is_normalize:
        _query=z_normalize(query)
    for i in range (1,N):
        #for k in range(m):
        if is_normalize:
            ts[i:m+i]=z_normalize(ts[i:m+i])
        dist_profile[i]=ED_distance(_query,ts[i:m+i])
    return dist_profile
