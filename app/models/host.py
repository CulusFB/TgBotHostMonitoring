import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


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
    names: list[Host]
    config_file: Path

    def __init__(self, config_file: Path) -> None:
        self.config_file = config_file
        self.names = []
        with config_file.open() as f:
            data = json.load(f).get("hosts")
        for host in data:
            self.names.append(Host(**host))

    def _save_config(self) -> None:
        with self.config_file.open() as f:
            json_data = json.load(f)
        json_data["hosts"] = [x.to_dict() for x in self.names]
        fd, tmp_path = tempfile.mkstemp(dir=self.config_file.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, 'w') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, self.config_file)
        except BaseException:
            os.unlink(tmp_path)
            raise

    def add_host(self, host: Host) -> list[Host]:
        self.names.append(host)
        self._save_config()
        return self.names

    def remove_host(self, host: Host) -> list[Host]:
        self.names.remove(host)
        self._save_config()
        return self.names

    def get_host(self, address: str) -> Optional[Host]:
        return next((x for x in self.names if x.address == address), None)

    def edit_host(self, host: Host) -> list[Host]:
        self._save_config()
        return self.names
