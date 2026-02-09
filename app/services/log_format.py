from app.models.host import Host


def host_name_address(host: Host) -> str:
    return f"имя: `{host.name}`, адрес: `{host.address}`"
