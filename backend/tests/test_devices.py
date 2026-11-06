from app.services import netbox

FAKE = [{"netbox_id": 1, "name": "cat8kv", "site": "DC-Lab",
         "platform": "ios", "mgmt_ip": "10.10.20.48"}]


def test_sync_creates_devices(client, monkeypatch):
    monkeypatch.setattr(netbox, "fetch_netbox_devices", lambda: FAKE)
    r = client.post("/devices/sync")
    assert r.json() == {"created": 1, "updated": 0, "total": 1}
    assert client.get("/devices").json()[0]["name"] == "cat8kv"


def test_sync_is_idempotent(client, monkeypatch):
    monkeypatch.setattr(netbox, "fetch_netbox_devices", lambda: FAKE)
    client.post("/devices/sync")
    r = client.post("/devices/sync")
    assert r.json() == {"created": 0, "updated": 1, "total": 1}
    assert len(client.get("/devices").json()) == 1