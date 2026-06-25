import networkx as nx
import numpy as np
from .equilibrium import compute_nash_equilibrium
from .cascade import nullification_cascade

class GRANullifier:
    def __init__(self, graph: nx.Graph, initial_suspicion: dict, 
                 influence_weight: float = 0.5, max_iter: int = 20, epsilon: float = 1e-4):
        self.graph = graph
        self.nodes = list(graph.nodes())
        self.node_index = {node: i for i, node in enumerate(self.nodes)}
        self.n = len(self.nodes)
        self.initial_suspicion = initial_suspicion
        self.influence_weight = influence_weight
        self.max_iter = max_iter
        self.epsilon = epsilon
        self.adj = nx.to_numpy_array(graph, nodelist=self.nodes, weight='weight')
        self.s0 = np.array([initial_suspicion.get(node, 0.0) for node in self.nodes])

    def run(self):
        equilibrium = compute_nash_equilibrium(self.adj, self.s0, self.influence_weight,
                                               self.max_iter, self.epsilon)
        nullified = nullification_cascade(self.graph, equilibrium, self.node_index,
                                          threshold=0.7, max_steps=5)
        return nullified
