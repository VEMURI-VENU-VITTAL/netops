import pytest
from app.config import settings
from app.models import Backup, Device, Job
from app.tasks.backup import clean_config, run_backup_job


@pytest.fixture(autouse=True)
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "backup_dir", str(tmp_path / "backups"))
    monkeypatch.setattr(settings, "mock_mode", True)


def setup_job(db):
    device = Device(netbox_id=1, name="r1", mgmt_ip="10.0.0.1", platform="ios")
    db.add(device)
    db.commit()
    job = Job(type="backup", device_id=device.id)
    db.add(job)
    db.commit()
    return device, job


def test_first_backup_creates_a_version(db_session):
    device, job = setup_job(db_session)
    run_backup_job(db_session, job)
    assert job.status == "succeeded"
    assert db_session.query(Backup).count() == 1
    assert device.last_backup_at is not None


def test_unchanged_config_adds_no_version(db_session):
    device, job = setup_job(db_session)
    run_backup_job(db_session, job)
    job2 = Job(type="backup", device_id=device.id)
    db_session.add(job2)
    db_session.commit()
    run_backup_job(db_session, job2)
    assert db_session.query(Backup).count() == 1
    assert "no change" in job2.log


def test_clean_config_strips_volatile_lines():
    raw = "Building configuration...\n\nCurrent configuration : 1234 bytes\n!\nhostname r1\n"
    cleaned = clean_config(raw)
    assert "Building" not in cleaned
    assert "Current configuration" not in cleaned
    assert "hostname r1" in cleaned