from http import HTTPStatus

from sqlalchemy.orm import Session

from user_todo_api.database import get_session
from user_todo_api.schemas import UserPublicSchema


def test_get_session():
    # Testa se o get_session retorna uma instância válida de Session
    session_from_get_session = next(get_session())
    assert isinstance(session_from_get_session, Session)

    # Testa se o objeto session_from_get_session foi criado corretamente
    assert session_from_get_session.bind is not None
    assert session_from_get_session.is_active


def test_create_user_success(client):
    # Testa a criação de um novo usuário
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,  # Assumindo que é o primeiro usuário criado
    }


def test_create_user_username_already_exists(client, user):
    # Testa a criação de um usuário com username já existente
    response = client.post(
        '/users/',
        json={
            'username': user.username,  # Usa o username da fixture 'user'
            'email': 'alice_new@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_already_exists(client, user):
    # Testa a criação de um usuário com email já existente
    response = client.post(
        '/users/',
        json={
            'username': 'alice_new',
            'email': user.email,  # Usa o email da fixture 'user'
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    # Faz uma requisição GET para a lista de usuários
    response = client.get('/users')

    # Verifica se a resposta é 200 OK
    assert response.status_code == HTTPStatus.OK

    # Verifica se a lista de usuários retornada está vazia (nenhum usuário no banco)
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    # Valida o usuário criado pela fixture e gera um dicionário com o schema esperado
    user_schema = UserPublicSchema.model_validate(user).model_dump()

    # Faz uma requisição GET para a lista de usuários
    response = client.get('/users/')

    # Verifica se a resposta contém o usuário criado na lista
    assert response.json() == {'users': [user_schema]}


def test_read_user_by_id(client, user_id, user):
    if user_id == 1:
        # Para o caso de user_id válido, usamos o usuário criado pela fixture
        response = client.get(f'/users/{user.id}')
        assert response.status_code == HTTPStatus.OK

        # Validamos os dados retornados
        user_schema = UserPublicSchema.model_validate(user).model_dump()
        assert response.json() == user_schema
    else:
        # Para o caso de user_id inválido (-1), esperamos 404 NOT FOUND
        response = client.get(f'/users/{user_id}')
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'detail': 'Usuário não encontrado'}


def test_update_user(client, user, user_id):
    if user_id == user.id:
        # Testa a atualização do usuário existente
        response = client.put(
            f'/users/{user.id}',
            json={
                'username': 'bob',
                'email': 'bob@example.com',
                'password': 'mynewpassword',
            },
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            'username': 'bob',
            'email': 'bob@example.com',
            'id': user.id,
        }
    else:
        # Testa a atualização com um user_id inválido
        response = client.put(
            f'/users/{user_id}',
            json={
                'username': 'bob',
                'email': 'bob@example.com',
                'password': 'mynewpassword',
            },
        )
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user, user_id):
    if user_id == user.id:
        # Testa a exclusão do usuário existente
        response = client.delete(f'/users/{user.id}')
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'message': 'User deleted'}
    else:
        # Testa a exclusão com um user_id inválido
        response = client.delete(f'/users/{user_id}')
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'detail': 'User not found'}
