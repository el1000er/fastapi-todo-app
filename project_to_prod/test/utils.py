
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
import pytest
from ..models import Todos,Users
from ..routers.auth import bcript_context

## create fake db
SQLALCHEMY_DATABASE_URL = "sqlite:///./project_3_alembic/test.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False},
    poolclass=StaticPool,
)

## testing session local, separate env that isolates from prod

TestingSessionLocal = sessionmaker(autocommit =False, autoflush =False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'admin','id':1,'user_role':'admin'}


## make sure our application is running as test
client = TestClient(app)

@pytest.fixture
def test_todo():
    ## Setup:
    ## Before the yield statement, you create a todo object and add it to the database.
    ## This part of the code sets up the necessary state for your test.
    todo =Todos(
        title='Learn to code!',
        description = 'Need to learn everyday',
        priority = 5,
        complete = False,
        owner_id = 1,
    )

    ## MAKE SURE THIS POINTS TO TEST CONNECTION DB NOT PRODUCTION OR OTHER DB!!!
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    ##Yield:
    ## The yield statement pauses the execution of the fixture and returns the todo object to the test function that uses this fixture.
    ## The test function can then use the todo object for its assertions and operations.
    yield todo
    # # Teardown:
    # # After the test function completes, the code after the yield statement is executed.
    # # In this case, it connects to the database and deletes all entries from the todos table to clean up the state.
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    ## Setup:
    ## Before the yield statement, you create a todo object and add it to the database.
    ## This part of the code sets up the necessary state for your test.
    user =Users(
        username="admin",
        email="admin@test.com", 
        first_name="ad",
        last_name="min",
        hashed_password=bcript_context.hash("asdzxc3033"),
        role="admin",
        phone_number ="(111)-111-1111"
    )
 
    ## MAKE SURE THIS POINTS TO TEST CONNECTION DB NOT PRODUCTION OR OTHER DB!!!
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    ##Yield:
    ## The yield statement pauses the execution of the fixture and returns the todo object to the test function that uses this fixture.
    ## The test function can then use the todo object for its assertions and operations.
    yield user
    # # Teardown:
    # # After the test function completes, the code after the yield statement is executed.
    # # In this case, it connects to the database and deletes all entries from the todos table to clean up the state.
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()