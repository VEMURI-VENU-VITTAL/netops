from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DeviceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    netbox_id: int
    name: str
    site: str | None
    platform: str | None
    mgmt_ip: str | None
    last_backup_at: datetime | None
    drift_status: str