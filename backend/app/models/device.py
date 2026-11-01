from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    netbox_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(String(100))
    site: Mapped[str] = mapped_column(String(100))
    platform: Mapped[str | None] = mapped_column(String(50))
    mgmt_ip: Mapped[str | None] = mapped_column(String(50))
    last_backup_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    drift_status: Mapped[str] = mapped_column(String(20), default="unknown")