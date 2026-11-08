from nornir.core import Nornir
from nornir.core.inventory import Defaults, Groups, Host, Hosts, Inventory
from nornir.plugins.runners import ThreadedRunner

from app.config import settings
from app.models import Device


def build_nornir(devices: list[Device]) -> Nornir:
    hosts = Hosts()
    for d in devices:
        hosts[d.name] = Host(
            name=d.name,
            hostname=d.mgmt_ip,
            platform=d.platform,
            username=settings.net_user,
            password=settings.net_pass,
            data={"device_id": d.id, "mgmt_ip": d.mgmt_ip},
        )
    inventory = Inventory(hosts=hosts, groups=Groups(), defaults=Defaults())
    return Nornir(inventory=inventory, runner=ThreadedRunner(num_workers=10))