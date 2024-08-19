from sqlalchemy.orm import Session

from user_todo_api.database import get_session


def test_get_session():
    # Testa se o get_session retorna uma instância válida de Session
    session_from_get_session = next(get_session())
    assert isinstance(session_from_get_session, Session)

    # Testa se o objeto session_from_get_session foi criado corretamente
    assert session_from_get_session.bind is not None
    assert session_from_get_session.is_active
