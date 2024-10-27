import numpy as np

from modules.utils import *

def top_k_motifs(matrix_profile: dict, top_k: int = 3, excl_zone: int = None) -> dict:
    """
    Find the top-k motifs based on matrix profile

    Parameters
    ---------
    matrix_profile: dict
        The matrix profile structure containing 'profile' (distances) and 'indices' (matches)
    top_k : int
        Number of motifs to find
    excl_zone : int
        Size of exclusion zone to avoid trivial matches

    Returns
    --------
    motifs: dict
        Dictionary containing "indices" and "distances" for the top-k motifs
    """

    # Extract matrix profile distances and indices
    profile_distances = matrix_profile["mp"]
    profile_indices = matrix_profile["mpi"]

    # Placeholder for results
    motifs_idx = []
    motifs_dist = []

    # Define a high value for exclusion zone replacements
    inf_value = np.inf

    # Find top-k motifs by iteratively finding the minimum distance and applying exclusion zones
    for _ in range(top_k):
        # Find the index of the minimum distance in profile_distances
        motif_idx = np.argmin(profile_distances)
        motif_dist = profile_distances[motif_idx]

        # Store the indices and distance
        motifs_idx.append((motif_idx, profile_indices[motif_idx]))
        motifs_dist.append(motif_dist)

        # Apply exclusion zone to avoid trivial matches around the found motif
        if excl_zone is not None:
            profile_distances = apply_exclusion_zone(profile_distances, motif_idx, excl_zone, inf_value)

    return {
        "indices": motifs_idx,
        "distances": motifs_dist
    }