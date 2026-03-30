def test_medicamentos_requiere_jwt(client):
    r = client.get("/api/medicamentos")
    assert r.status_code == 401


def test_medicamentos_con_token(client, auth_headers):
    r = client.get("/api/medicamentos", headers=auth_headers)
    assert r.status_code == 200
    items = r.get_json()
    assert len(items) == 2
    assert any(m["nombre"] == "Acetaminofén" and m["es_pos"] is True for m in items)


def test_crear_solicitud_pos(client, auth_headers):
    r = client.post(
        "/api/solicitudes",
        headers=auth_headers,
        json={"medicamento_id": 1},
    )
    assert r.status_code == 201
    body = r.get_json()
    assert body["medicamento_nombre"] == "Acetaminofén"
    assert body["es_pos"] is True


def test_crear_solicitud_no_pos_sin_campos(client, auth_headers):
    r = client.post(
        "/api/solicitudes",
        headers=auth_headers,
        json={"medicamento_id": 2},
    )
    assert r.status_code == 400


def test_crear_solicitud_no_pos_ok(client, auth_headers):
    r = client.post(
        "/api/solicitudes",
        headers=auth_headers,
        json={
            "medicamento_id": 2,
            "numero_orden": "ORD-1",
            "direccion": "Calle 1",
            "telefono": "3001234567",
            "correo": "paciente@example.com",
        },
    )
    assert r.status_code == 201
    assert r.get_json()["es_pos"] is False


def test_listar_solicitudes_paginado(client, auth_headers):
    client.post("/api/solicitudes", headers=auth_headers, json={"medicamento_id": 1})
    r = client.get("/api/solicitudes?page=1&per_page=10", headers=auth_headers)
    assert r.status_code == 200
    data = r.get_json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1
    assert "medicamento_nombre" in data["items"][0]
