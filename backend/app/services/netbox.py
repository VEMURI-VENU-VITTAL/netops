import pynetbox
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Device


def fetch_netbox_devices() -> list[dict]:
    if not settings.netbox_token:
        raise RuntimeError("NETBox token not set!")
    nb = pynetbox.api(settings.netbox_url, token=settings.netbox_token)
    filters = {"site":settings.netbox_site} if settings.netbox_site else {}
    records = []

    for d in nb.dcim.devices.filters(**filters):
        if not d.name:
            continue
        records.append({
            "netbox_id":d.id,
            "name":d.name,
            "site":d.site.name if d.site else None,
            "platform":d.platform.slug if d.platform else None,
            "mgmt_ip": str(d.primary_ip4.address).split("/")[0] if d.primary_ip4 else None
        })

    return records 

def upsert_devices(db:Session, records:list[dict]) -> dict:
    created = updated = 0
    for rec in records:
        dev = db.scalar(select(Device).where(Device.netbox_id==rec["netbox_id"]))
        if dev is None:
            db.add(Device(**rec))
            created+=1
        else:
            for key, value in rec.items():
                setattr(dev, key, value)
            updated+=1
    db.commit()
    return {"created": created, "updated": updated, "total": len(records)}
