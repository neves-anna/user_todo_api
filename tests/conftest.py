import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from user_todo_api.app import app
from user_todo_api.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(params=[1, -1])  # Testa com user_id válido e inválido
def user_id(request):
    return request.param


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
