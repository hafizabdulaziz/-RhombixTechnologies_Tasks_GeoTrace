import os
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine, Index
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

# Database URL
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_SQLITE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'geoengine.db')}"

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

def get_engine(url=None):
    db_url = url or os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)
    if db_url.startswith("sqlite"):
        return create_engine(
            db_url, 
            connect_args={"check_same_thread": False},
            pool_pre_ping=True
        )
    else:
        # PostgreSQL: Force usage of psycopg2 driver
        if db_url.startswith(("postgresql://", "postgres://")):
            db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1).replace("postgres://", "postgresql+psycopg2://", 1)
        return create_engine(db_url, pool_pre_ping=True)

# Default engine and session factory
engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db(engine_instance=None):
    """Create tables if they don't exist (only for SQLite)."""
    target_engine = engine_instance or engine
    db_url = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)
    if db_url.startswith("sqlite"):
        Base.metadata.create_all(target_engine)
