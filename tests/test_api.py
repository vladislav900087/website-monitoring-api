

def test_get_health(client):

    response = client.get('/health')

    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

# authentication

def test_register_user(client):

    response = client.post('/monitoring-api/auth/register', json={'email': 'test_user@example.com', 'password': "hashed"})

    assert response.status_code == 201
    assert response.json()['email'] == 'test_user@example.com'

def test_register_already_registered(client):

    response = client.post('/monitoring-api/auth/register', json={'email': 'test_user@example.com', 'password': 'hashed'})

    assert response.status_code == 201

    response = client.post('/monitoring-api/auth/register', json={'email': 'test_user@example.com', 'password': 'hashed'})

    assert response.status_code == 409

def test_login(client):

    register_response = client.post('/monitoring-api/auth/register', json={'email': 'test_user@example.com', 'password': 'hashed'})

    assert register_response.status_code == 201

    login_response = client.post('/monitoring-api/auth/login', data={"username": 'test_user@example.com', 'password': 'hashed'})

    assert login_response.status_code == 200

def test_login_with_invalid_credentials(client):

    register_response = client.post('/monitoring-api/auth/register', json={'email': 'test_user@example.com', 'password': 'hashed'})

    assert register_response.status_code == 201

    login_response = client.post('/monitoring-api/auth/login', data={'username': 'test_user@example.com', 'password': 'invalid'})

    assert login_response.status_code == 401
    assert login_response.json() == {'detail': 'Invalid credentials'}

def test_get_current_user(client):

    register_response = client.post('/monitoring-api/auth/register', json={'email': 'test_user@example.com', 'password': 'hashed'})

    assert register_response.status_code == 201

    login_response = client.post('/monitoring-api/auth/login', data={'username': 'test_user@example.com', 'password': 'hashed'})

    assert login_response.status_code == 200

    token = login_response.json()['access_token']

    assert isinstance(token, str)


    get_response = client.get('/monitoring-api/auth/me', headers={'Authorization': f'Bearer {token}'})


    assert get_response.status_code == 200
    assert get_response.json()['email'] == 'test_user@example.com'

