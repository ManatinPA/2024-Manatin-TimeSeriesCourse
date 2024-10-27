import numpy as np

from modules.utils import *

def top_k_discords(matrix_profile: dict, top_k: int = 3) -> dict:
    """
    Find the top-k discords based on matrix profile

    Parameters
    ---------
    matrix_profile: dict
        The matrix profile structure containing 'profile' (distances) and 'indices' (nearest neighbors)
    top_k : int
        Number of discords to find
    excl_zone : int
        Size of exclusion zone to avoid trivial matches

    Returns
    --------
    discords: dict
        Dictionary containing "indices", "distances" and "nn_indices" for the top-k discords
    """

    # Extract matrix profile distances and indices
    profile_distances = np.copy(matrix_profile['mp'])
    profile_indices = matrix_profile['mpi']

    # Placeholder for results
    discords_idx = []
    discords_dist = []
    discords_nn_idx = []

    # Define a low value for exclusion zone replacements to avoid them being selected
    neg_inf_value = -np.inf

    # Find top-k discords by iteratively finding the maximum distance and applying exclusion zones
    for _ in range(top_k):
        # Find the index of the maximum distance in profile_distances
        discord_idx = np.argmax(profile_distances)
        discord_dist = profile_distances[discord_idx]
        nn_idx = profile_indices[discord_idx]

        # Store the indices, distance, and nearest neighbor index
        discords_idx.append(discord_idx)
        discords_dist.append(discord_dist)
        discords_nn_idx.append(nn_idx)


        profile_distances = apply_exclusion_zone(profile_distances, discord_idx, matrix_profile['excl_zone'], neg_inf_value)

    return {
        "indices": discords_idx,
        "distances": discords_dist,
        "nn_indices": discords_nn_idx
    }