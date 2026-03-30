def test_register_y_login(client):
    r = client.post(
        "/auth/register",
        json={"email": "nuevo@example.com", "password": "clave12345"},
    )
    assert r.status_code == 201
    body = r.get_json()
    assert "access_token" in body
    assert body["user"]["email"] == "nuevo@example.com"

    r2 = client.post(
        "/auth/login",
        json={"email": "nuevo@example.com", "password": "clave12345"},
    )
    assert r2.status_code == 200
    assert "access_token" in r2.get_json()


def test_register_email_invalido(client):
    r = client.post(
        "/auth/register",
        json={"email": "no-es-email", "password": "clave12345"},
    )
    assert r.status_code == 400


def test_register_password_corta(client):
    r = client.post(
        "/auth/register",
        json={"email": "ok@example.com", "password": "corta"},
    )
    assert r.status_code == 400


def test_login_credenciales_malas(client):
    r = client.post(
        "/auth/login",
        json={"email": "nadie@example.com", "password": "wrongpassword"},
    )
    assert r.status_code == 401
