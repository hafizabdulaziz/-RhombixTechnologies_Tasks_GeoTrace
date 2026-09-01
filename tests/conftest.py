import os
import pytest
from src.database.models import Base, get_engine, SessionLocal
import src.database.models

# Force SQLite for testing
@pytest.fixture(scope="session", autouse=True)
def setup_db():
    test_db_url = "sqlite:///./test.db"
    os.environ["DATABASE_URL"] = test_db_url
    
    # Reconfigure the engine and session factory
    new_engine = get_engine(test_db_url)
    src.database.models.engine = new_engine
    src.database.models.SessionLocal.configure(bind=new_engine)
    
    # Create tables on the test engine
    Base.metadata.create_all(new_engine)
    yield
    
    # Cleanup
    Base.metadata.drop_all(new_engine)
    if os.path.exists("./test.db"):
        try:
            os.remove("./test.db")
        except PermissionError:
            pass
