import os
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine, Index
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

# Database URL
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_SQLITE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'geoengine.db')}"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)

Base = declarative_base()

class LookupHistory(Base):
    __tablename__ = 'lookup_history'
    id = Column(Integer, primary_key=True)
    ip = Column(String, index=True, nullable=False)
    city = Column(String, nullable=True)
    region = Column(String, nullable=True)
    country = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    provider = Column(String, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), index=True)

    __table_args__ = (
        Index('idx_ip_timestamp', 'ip', 'timestamp'),
    )

# Dynamic Engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False},
        pool_pre_ping=True
    )
else:
    # PostgreSQL: Force usage of psycopg (v3) driver
    if DATABASE_URL.startswith(("postgresql://", "postgres://")):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1).replace("postgres://", "postgresql+psycopg://", 1)
        
    engine = create_engine(
        DATABASE_URL, 
        pool_pre_ping=True
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create tables if they don't exist (only for SQLite)."""
    # SQLite ke liye database file generate karni hai
    if DATABASE_URL.startswith("sqlite"):
        Base.metadata.create_all(engine)
    # PostgreSQL migrations are managed via deployment-time CLI commands.
