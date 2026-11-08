import pynetbox

# from app.config import settings

nb = pynetbox.api("https://demo.netbox.dev", token = "nbt_8xCZDTxCnfjk.RxzKWjqTDMxRIabzNpMFgeFUx2KfOJxfEVeValxD")

def get_or_create(endpoint, lookup, **extra):
    return endpoint.get(**lookup) or endpoint.create(**lookup, **extra)

site = get_or_create(nb.dcim.sites, {"slug":"dc-lab"}, name="DC-Lab")
mfr = get_or_create(nb.dcim.manufacturers, {"slug":"cisco"}, name="Cisco")
dtype = get_or_create(nb.dcim.device_types, {"slug": "c8000v"},
                      model="C8000V", manufacturer=mfr.id)

role = get_or_create(nb.dcim.device_roles, {"slug":"router"}, name="Router", color="2196f3")
plat = get_or_create(nb.dcim.platforms, {"slug":"cisco-ios"}, name="cisco_ios")

dev = get_or_create(nb.dcim.devices, {"name": "cat8kv", "site_id": site.id},
                    device_type=dtype.id, role=role.id, platform=plat.id,
                    status="active") if False else (
      nb.dcim.devices.get(name="cat8kv", site_id=site.id) or
      nb.dcim.devices.create(name="cat8kv", site=site.id, device_type=dtype.id,
                             role=role.id, platform=plat.id, status="active"))

intf = (nb.dcim.interfaces.get(device_id=dev.id, name="GigabitEthernet1") or
        nb.dcim.interfaces.create(device=dev.id, name="GigabitEthernet1", type="virtual"))

ip = (nb.ipam.ip_addresses.get(address="10.10.20.48/24", interface_id=intf.id) or
      nb.ipam.ip_addresses.create(address="10.10.20.48/24",
                                  assigned_object_type="dcim.interface",
                                  assigned_object_id=intf.id))

loopback1 = (nb.dcim.interfaces.get(device_id=dev.id, name="Loopback1") or
    nb.dcim.interfaces.create(device=dev.id, name="Loopback1", type="virtual"))

loopback1_ip = (
    nb.ipam.ip_addresses.get(address="1.1.1.1/32")
    or
    nb.ipam.ip_addresses.create(
        address="1.1.1.1/32",
        assigned_object_type="dcim.interface",
        assigned_object_id=loopback1.id
    )
)


dev.primary_ip4 = ip.id
dev.platform = plat.id
dev.save()