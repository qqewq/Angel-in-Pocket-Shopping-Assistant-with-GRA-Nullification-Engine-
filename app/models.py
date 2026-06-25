from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from .database import Base
import enum
import datetime

class SubscriptionTier(str, enum.Enum):
    free = "free"
    basic = "basic"
    premium = "premium"
    enterprise = "enterprise"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.free)
    stripe_customer_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    reviews = relationship("Review", back_populates="author")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    price = Column(Float)
    description = Column(String)
    category = Column(String)
    seller_id = Column(Integer, ForeignKey("sellers.id"))
    seller = relationship("Seller", back_populates="products")
    reviews = relationship("Review", back_populates="product")

class Seller(Base):
    __tablename__ = "sellers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    rating = Column(Float, default=0.0)
    account_age_days = Column(Integer)
    products = relationship("Product", back_populates="seller")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    rating = Column(Float)
    sentiment_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    author_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    author = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    stripe_subscription_id = Column(String, unique=True)
    plan = Column(String)
    status = Column(String)
    current_period_end = Column(DateTime)
