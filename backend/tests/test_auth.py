from app.auth import hash_password
from app.models import User


def add_user(db):
    db.add(User(username="admin", password_hash=hash_password("secret"), role="admin"))
    db.commit()


def test_login_and_me(anon_client, db_session):
    add_user(db_session)
    r = anon_client.post("/auth/login", data={"username": "admin", "password": "secret"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    me = anon_client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.json() == {"username": "admin", "role": "admin"}


def test_wrong_password_rejected(anon_client, db_session):
    add_user(db_session)
    r = anon_client.post("/auth/login", data={"username": "admin", "password": "nope"})
    assert r.status_code == 401


def test_devices_require_login(anon_client):
    assert anon_client.get("/devices").status_code == 401