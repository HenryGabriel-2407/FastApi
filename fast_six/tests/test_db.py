from sqlalchemy import select

from fast_six.models import User


def test_db(session):
    user = User(username='henrygabriel', email='henrygabriel@gmail.com', password='minha_senha-legal')
    session.add(user)
    session.commit()
    session.refresh(user)

    result = session.scalar(select(User).where(User.username == 'henrygabriel'))

    assert result.email == 'henrygabriel@gmail.com'
