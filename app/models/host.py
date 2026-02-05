import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Host:
    name: str
    address: str


class Hosts:
    names: list[Host] = []
    config_file: Path

    def __init__(self, config_file: Path) -> None:
        self.config_file = config_file
        with config_file.open() as f:
            data = json.load(f).get("hosts")
        for host in data:
            self.names.append(Host(**host))

    def save_config(self) -> None:
        with self.config_file.open('w') as f:
            json.dump(self.names, f)

    def add_host(self, host: Host) -> None:
        self.names.append(host)
        self.save_config()

    def remove_host(self, host: Host) -> None:
        self.names.remove(host)
        self.save_config()
