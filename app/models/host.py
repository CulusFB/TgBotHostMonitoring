import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Host:
    name: str
    address: str
    status: bool

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "address": self.address,
            "status": self.status
        }


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
        with self.config_file.open() as f:
            json_data = json.load(f)
        json_data["hosts"] = [x.to_dict() for x in self.names]
        with self.config_file.open('w') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

    def add_host(self, host: Host) -> None:
        self.names.append(host)
        self.save_config()

    def remove_host(self, host: Host) -> list[Host]:
        self.names.remove(host)
        print(self.names)
        self.save_config()
        return self.names

    def get_host(self, address: str) -> Host:
        return [x for x in self.names if x.address == address][0]
    # def edit_host(self,host:Host) -> list[Host]:
