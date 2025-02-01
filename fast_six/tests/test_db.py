import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from fast_six.models import User, table_registry


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    table_registry.metadata.drop_all(engine)


def test_db(session):
    user = User(username='henrygabriel', email='henrygabriel@gmail.com', password='minha_senha-legal')
    session.add(user)
    session.commit()
    session.refresh(user)

    result = session.scalar(select(User).where(User.username == 'henrygabriel'))

    assert result.email == 'henrygabriel@gmail.com'
