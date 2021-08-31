import pytest

from api import Request
from api.funcs import generate, generate_id
from api.models.user import User, process_lower
from api.methods.account.bot import handle
# from api.errors import ErrorWrong


@pytest.mark.asyncio
async def test_repeated_login():
    login = generate(20)
    user_old = User(login=login)

    user_old.save()
    assert user_old.id
    assert user_old.login == process_lower(login)

    request = Request(None, None, generate(), 2, 0)
    data = {
        'user': generate_id(),
        'login': login.upper(),
    }

    res = await handle(None, request, data)

    assert res.get('id')
    assert res.get('new')

    user_new = User.get(ids=res['id'], fields={'login'})

    assert user_new.login != process_lower(login)
    assert user_new.id != user_old.id
