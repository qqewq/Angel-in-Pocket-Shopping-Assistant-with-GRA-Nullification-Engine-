from sqlalchemy.orm import Session
from .graph_builder import build_subgraph_for_product
from .gra_adapter import run_nullification

def evaluate_product_safety(product_id: int, db: Session, user_tier: str = "free") -> dict:
    depth_map = {"free": 1, "basic": 1, "premium": 2, "enterprise": 3}
    depth = depth_map.get(user_tier, 1)

    graph, suspicion = build_subgraph_for_product(product_id, db, depth=depth)
    nullification = run_nullification(graph, suspicion)

    adv_degree = nullification.get(product_id, 0.0)
    trust_score = round(max(0.0, 1.0 - adv_degree), 4)

    result = {
        "product_id": product_id,
        "trust_score": trust_score,
        "adversarial_degree": round(adv_degree, 4),
    }
    if user_tier in ("premium", "enterprise"):
        seller_id = next((n for n in graph.neighbors(product_id) if graph.nodes[n].get('type')=='seller'), None)
        if seller_id:
            result["seller_trust"] = round(1.0 - nullification.get(seller_id, 0.0), 4)
        suspicious_reviews = [n for n in graph.neighbors(product_id)
                              if graph.nodes[n].get('type')=='review' and nullification.get(n,0)>0.7]
        result["suspicious_reviews_count"] = len(suspicious_reviews)

    return result
