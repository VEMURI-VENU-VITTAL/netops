import hashlib
from datetime import UTC, datetime
from pathlib import Path

from nornir.core.task import Result, Task
from nornir_netmiko.tasks import netmiko_send_command
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.db import SessionLocal
from app.models import Backup, Device, Job
from app.services import git_store
from app.services.nornir_runner import build_nornir

MOCK_DIR = Path(__file__).parent.parent / "mock_devices"
VOLATILE_PREFIXES = (
    "Building configuration",
    "Current configuration",
    "! Last configuration change",
    "! NVRAM config last updated",
)


def now() -> datetime:
    return datetime.now(UTC)


def clean_config(text: str) -> str:
    """Drop lines that change on every run, so they don't show up as fake diffs."""
    lines = [line for line in text.splitlines() if not line.startswith(VOLATILE_PREFIXES)]
    return "\n".join(lines).strip() + "\n"


def mock_running_config(task: Task) -> str:
    custom = MOCK_DIR / f"{task.host.name}.cfg"
    if custom.exists():
        return custom.read_text()
    return (f"hostname {task.host.name}\n!\n"
            f"interface GigabitEthernet1\n"
            f" ip address {task.host.data['mgmt_ip']} 255.255.255.0\n!\nend\n")


def get_config(task: Task) -> Result:
    if settings.mock_mode:
        config = mock_running_config(task)
    else:
        config = task.run(task=netmiko_send_command,
                          command_string="show running-config").result
    return Result(host=task.host, result=config)


def run_backup_job(db: Session, job: Job) -> None:
    job.status, job.started_at = "running", now()
    db.commit()

    query = select(Device)
    if job.device_id:
        query = query.where(Device.id == job.device_id)
    devices = list(db.scalars(query).all())

    results = build_nornir(devices).run(task=get_config)

    log, failed = [], 0
    for d in devices:
        multi = results[d.name]
        if multi.failed:
            failed += 1
            log.append(f"{d.name}: FAILED - {multi[0].exception}")
            continue

        config = clean_config(multi.result)
        commit, changed = git_store.save_config(d.name, config)
        has_backup = db.scalar(select(Backup.id).where(Backup.device_id == d.id))
        if changed or not has_backup:
            data = config.encode()
            db.add(Backup(device_id=d.id, git_commit=commit,
                          sha256=hashlib.sha256(data).hexdigest(), size_bytes=len(data)))
        d.last_backup_at = now()
        log.append(f"{d.name}: {'changed' if changed else 'no change'} ({commit[:8]})")

    job.status = "failed" if failed else "succeeded"
    job.finished_at = now()
    job.log = "\n".join(log) or "No devices"
    db.commit()


def run_backup(job_id: int) -> None:
    """Entry point the worker calls (Step 11)."""
    with SessionLocal() as db:
        job = db.get(Job, job_id)
        try:
            run_backup_job(db, job)
        except Exception as e:
            db.rollback()
            job.status, job.finished_at = "failed", now()
            job.log = f"Job crashed: {e}"
            db.commit()
            raise