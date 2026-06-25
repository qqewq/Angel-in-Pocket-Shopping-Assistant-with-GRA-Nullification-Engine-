import networkx as nx
from sqlalchemy.orm import Session
from datetime import datetime
from .models import Product, Seller, Review, User

def build_subgraph_for_product(product_id: int, db: Session, depth: int = 2):
    G = nx.Graph()
    suspicion = {}
    visited = set()

    def traverse_product(pid, current_depth):
        if current_depth > depth or pid in visited:
            return
        visited.add(pid)
        product = db.query(Product).get(pid)
        if not product:
            return
        G.add_node(pid, type='product', label=product.title)
        susp = 0.1
        if product.price < 5:
            susp += 0.2
        suspicion[pid] = min(susp, 1.0)

        seller = product.seller
        if seller:
            sid = f"seller_{seller.id}"
            if sid not in G:
                G.add_node(sid, type='seller', label=seller.name)
                age_susp = max(0, 1 - seller.account_age_days/365)
                suspicion[sid] = 0.1 + age_susp * 0.3
            G.add_edge(pid, sid, weight=0.8, relation='sells')

            if current_depth < depth:
                for other_product in seller.products:
                    if other_product.id != pid:
                        traverse_product(other_product.id, current_depth+1)

        reviews = db.query(Review).filter(Review.product_id == pid).all()
        for rev in reviews:
            rid = f"review_{rev.id}"
            G.add_node(rid, type='review', label=rev.text[:30])
            rev_susp = 0.1
            if rev.rating <= 1 or rev.rating >= 5:
                rev_susp += 0.2
            if rev.sentiment_score and abs(rev.sentiment_score) > 0.9:
                rev_susp += 0.1
            suspicion[rid] = min(rev_susp, 1.0)
            G.add_edge(pid, rid, weight=0.5, relation='has_review')

            user = rev.author
            if user:
                uid = f"user_{user.id}"
                if uid not in G:
                    G.add_node(uid, type='user', label=user.email)
                    days_active = (datetime.utcnow() - user.created_at).days
                    user_susp = max(0, 1 - days_active/180)
                    suspicion[uid] = user_susp
                G.add_edge(uid, rid, weight=0.7, relation='wrote')

    traverse_product(product_id, 0)
    return G, suspicion
