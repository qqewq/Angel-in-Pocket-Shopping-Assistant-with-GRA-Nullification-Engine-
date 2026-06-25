def nullification_cascade(graph, equilibrium, node_index, threshold=0.7, max_steps=5):
    nullified = {node: 0.0 for node in graph.nodes()}
    active = set()
    for node, idx in node_index.items():
        if equilibrium[idx] > threshold:
            nullified[node] = 1.0
            active.add(node)
    for _ in range(max_steps):
        if not active:
            break
        next_active = set()
        for node in active:
            for neighbor in graph.neighbors(node):
                if nullified[neighbor] >= 1.0:
                    continue
                weight = graph[node][neighbor].get('weight', 1.0)
                nullified[neighbor] = min(1.0, nullified[neighbor] + weight * 0.5)
                if nullified[neighbor] >= 1.0:
                    next_active.add(neighbor)
        active = next_active
    return nullified
