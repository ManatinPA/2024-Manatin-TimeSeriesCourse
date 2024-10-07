import numpy as np


def ED_distance(ts1: np.ndarray, ts2: np.ndarray) -> float:
    """
    Calculate the Euclidean distance

    Parameters
    ----------
    ts1: the first time series
    ts2: the second time series

    Returns
    -------
    ed_dist: euclidean distance between ts1 and ts2
    """
    
    ed_dist = np.linalg.norm(ts2-ts1)
    # INSERT YOUR CODE

    return ed_dist


def norm_ED_distance(ts1: np.ndarray, ts2: np.ndarray) -> float:
    """
    Calculate the normalized Euclidean distance

    Parameters
    ----------
    ts1: the first time series
    ts2: the second time series

    Returns
    -------
    norm_ed_dist: normalized Euclidean distance between ts1 and ts2s
    """

    norm_ed_dist = np.sqrt(abs(2*ts1.size*
    (1-(np.dot(ts1,ts2)-ts1.size*np.mean(ts1)*np.mean(ts2)/
    (ts1.size*np.std(ts1)*np.std(ts2))))))

    # INSERT YOUR CODE

    return norm_ed_dist


def DTW_distance(ts1: np.ndarray, ts2: np.ndarray, w: float = None) -> float:
    """
    Calculate DTW distance

    Parameters
    ----------
    ts1: first time series
    ts2: second time series
    r: warping window size
    
    Returns
    -------
    dtw_dist: DTW distance between ts1 and ts2
    """

    n, m = len(ts1), len(ts2)
    
    # Если не задано окно, ставим максимальное возможное
    if w is None:
        w = max(n, m)
    else:
        w = max(int(w), abs(n - m))  # Ширина полосы должна учитывать разницу в длине

    # Инициализация матрицы расстояний
    dtw_matrix = np.full((n + 1, m + 1), np.inf)
    dtw_matrix[0, 0] = 0

    # Заполняем матрицу расстояний с учетом полосы Сако-Чиба
    for i in range(1, n + 1):
        for j in range(max(1, i - w), min(m + 1, i + w + 1)):
            cost = (ts1[i - 1] - ts2[j - 1]) ** 2  # Евклидово расстояние (квадрат разности)
            dtw_matrix[i, j] = cost + min(float(dtw_matrix[i - 1, j]),    # Вставка
                                          float(dtw_matrix[i, j - 1]),    # Удаление
                                          float(dtw_matrix[i - 1, j - 1]))  # Совпадение

    # Финальное расстояние DTW
    return dtw_matrix[n, m]