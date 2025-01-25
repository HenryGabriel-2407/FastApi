from fast_four.security import ALGORITM, SECRET_KEY, create_acess_token
from jwt import decode


def test_jwt():
    data = {'sub': 'test@example.com'}
    token = create_acess_token(data)
    result = decode(token, SECRET_KEY, algoritms=[ALGORITM])
    assert result['sub'] == data['sub']
    assert result['exp']
