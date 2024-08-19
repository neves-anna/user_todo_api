from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
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
        'id': 1,
    }


def test_read_all_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'id': 1,
            }
        ]
    }


def test_read_user_by_id(client, user_id):
    # Se o user_id for válido (1), primeiro criamos um usuário
    if user_id == 1:
        response = client.post(
            '/users/',
            json={
                'username': 'alice',
                'email': 'alice@example.com',
                'password': 'alicepassword',
            },
        )
        assert response.status_code == HTTPStatus.CREATED
        created_user_id = response.json()['id']
    else:
        created_user_id = user_id  # Para o caso de user_id inválido, usamos o valor diretamente

    response = client.get(f'/users/{created_user_id}')

    if user_id == 1:
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            'username': 'alice',
            'email': 'alice@example.com',
            'id': created_user_id,
        }
    else:
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'detail': 'Usuario não encontrado'}


def test_update_user(client, user_id):
    response = client.put(
        f'/users/{user_id}',
        json={
            'username': 'bob' if user_id == 1 else 'invalid',
            'email': 'bob@example.com' if user_id == 1 else 'invalid@example.com',
            'password': 'mynewpassword' if user_id == 1 else 'invalid',
        },
    )

    if user_id == 1:
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            'username': 'bob',
            'email': 'bob@example.com',
            'id': 1,
        }
    else:
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'detail': 'Usuario não encontrado'}


def test_delete_user(client, user_id):
    response = client.delete(f'/users/{user_id}')

    if user_id == 1:
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'message': 'Usuario deletado'}
    else:
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'detail': 'Usuario não encontrado'}
