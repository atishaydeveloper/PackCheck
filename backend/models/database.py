"""
Database models for PackCheck
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, JSON, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

class User(Base):
    """User profile model"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Fitness profile
    fitness_goal = Column(String(50))  # muscle_building, weight_loss, maintenance
    weight = Column(Float)  # kg
    height = Column(Float)  # cm
    age = Column(Integer)
    gender = Column(String(20))

    # Relationships
    scans = relationship("Scan", back_populates="user")
    profiles = relationship("UserProfile", back_populates="user")

class UserProfile(Base):
    """Detailed user profile with workout schedule and preferences"""
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Workout schedule (JSON)
    workout_schedule = Column(JSON)

    # Dietary preferences (JSON)
    dietary_preferences = Column(JSON)

    # Calculated targets (JSON)
    nutrition_targets = Column(JSON)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="profiles")

class Product(Base):
    """Product information model"""
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    product_id = Column(String(100), unique=True, nullable=False)

    # Product metadata
    name = Column(String(255))
    brand = Column(String(255))
    category = Column(String(100))
    barcode = Column(String(50))

    # Nutrition facts (JSON)
    nutrition_facts = Column(JSON)

    # Ingredients
    ingredients = Column(Text)

    # FSSAI verification
    fssai_verified = Column(Boolean, default=False)
    fssai_verification_data = Column(JSON)

    # Community verification
    community_verified = Column(Boolean, default=False)
    community_verification_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    scans = relationship("Scan", back_populates="product")

class Scan(Base):
    """Scan history model"""
    __tablename__ = 'scans'

    id = Column(Integer, primary_key=True)
    scan_id = Column(String(100), unique=True, nullable=False)

    # Foreign keys
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))

    # Scan data
    image_path = Column(String(500))
    ocr_results = Column(JSON)
    confidence_scores = Column(JSON)

    # FSSAI verification results
    fssai_verification = Column(JSON)

    # Personalization
    workout_timing = Column(String(50))  # pre_workout, post_workout, etc.
    personalized_recommendations = Column(JSON)

    # Timestamps
    scanned_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="scans")
    product = relationship("Product", back_populates="scans")

class CommunityVerification(Base):
    """Community verification submissions"""
    __tablename__ = 'community_verifications'

    id = Column(Integer, primary_key=True)
    verification_id = Column(String(100), unique=True, nullable=False)

    # Foreign keys
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    # Verification data
    verification_type = Column(String(50))  # confirm, correct, flag
    corrected_data = Column(JSON)
    confidence = Column(String(20))  # low, medium, high

    # Review status
    status = Column(String(20), default='pending')  # pending, approved, rejected
    dietitian_verified = Column(Boolean, default=False)
    dietitian_id = Column(String(100))
    dietitian_notes = Column(Text)

    # Timestamps
    submitted_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime)

class NutritionLog(Base):
    """Daily nutrition tracking log"""
    __tablename__ = 'nutrition_logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Date
    log_date = Column(DateTime, nullable=False)

    # Daily totals
    total_calories = Column(Float, default=0)
    total_protein = Column(Float, default=0)
    total_carbs = Column(Float, default=0)
    total_fat = Column(Float, default=0)
    total_sugar = Column(Float, default=0)

    # Meal breakdown (JSON)
    meals = Column(JSON)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Database initialization
def init_db(database_url=None):
    """Initialize database and create tables"""
    if database_url is None:
        database_url = os.getenv('DATABASE_URL', 'postgresql://localhost/packcheck')

    engine = create_engine(database_url)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    return Session()

# Database session helper
def get_db_session():
    """Get database session"""
    database_url = os.getenv('DATABASE_URL', 'sqlite:///packcheck.db')
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    return Session()
