from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./ecointellect.db"

# SQLite requires check_same_thread=False for FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class OrderRecord(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, default="user_demo")
    distance_km = Column(Float)
    transport_mode = Column(String)
    packaging_type = Column(String)
    carbon_emission_grams = Column(Float)
    eco_score = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create tables immediately
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
