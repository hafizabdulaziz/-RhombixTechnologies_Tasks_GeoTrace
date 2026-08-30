import os
import pytest
from sqlalchemy import create_engine
from src.database.models import Base

# Force SQLite for testing
@pytest.fixture(scope="session", autouse=True)
def setup_db():
    os.environ["DATABASE_URL"] = "sqlite:///./test.db"
    # Create the test database
    engine = create_engine("sqlite:///./test.db")
    Base.metadata.create_all(engine)
    yield
    # Cleanup
    engine.dispose()
    if os.path.exists("./test.db"):
        try:
            os.remove("./test.db")
        except PermissionError:
            pass # File still locked, skip deletion
