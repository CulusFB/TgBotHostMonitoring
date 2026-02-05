import json
from pathlib import Path


class Hosts:
    names: list[str]
    config_file: Path

    def __init__(self, config_file: Path):
        self.config_file = config_file
        with config_file.open() as f:
            self.names = json.load(f).get("hosts")

    def save_config(self):
        with self.config_file.open('w') as f:
            json.dump(self.names, f)

    def add_host(self, host: str):
        self.names.append(host)
        self.save_config()

    def remove_host(self, host: str):
        self.names.remove(host)
        self.save_config()
