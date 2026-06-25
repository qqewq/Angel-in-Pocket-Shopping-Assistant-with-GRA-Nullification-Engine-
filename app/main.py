from fastapi import FastAPI
from .routers import auth, products, sellers, reviews, subscriptions
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Angel-in-Pocket with GRA Engine")

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(sellers.router)
app.include_router(reviews.router)
app.include_router(subscriptions.router)
