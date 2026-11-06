from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Device
from app.schemas.device import DeviceOut
from app.services import netbox

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("", response_model=list[DeviceOut])
def list_devices(
        db: Session = Depends(get_db) # noqa: B008
    ):
    return db.scalars(select(Device).order_by(Device.name)).all()


@router.post("/sync")
def sync_devices(
        db: Session = Depends(get_db) # noqa: B008
    ):
    try:
        records = netbox.fetch_netbox_devices()
    except ConnectionError as e:
        raise HTTPException(status_code=502, detail=f"NetBox sync failed: {e}")
    return netbox.upsert_devices(db, records)