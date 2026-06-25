from gra_engine.core import GRANullifier
from .config import settings

def run_nullification(graph, suspicion):
    nullifier = GRANullifier(
        graph,
        suspicion,
        influence_weight=settings.GRA_INFLUENCE_WEIGHT,
        max_iter=settings.GRA_MAX_ITER,
        epsilon=settings.GRA_EPSILON
    )
    return nullifier.run()
