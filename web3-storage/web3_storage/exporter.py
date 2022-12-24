from prometheus_client import start_http_server, Gauge
from time import sleep
import requests


class Web3StorageExporter:
    def __init__(self, token: str, port: int = 9325, host: str = "0.0.0.0"):
        self.token = token
        self.port = port
        self.host = host
        self.direct_gauge = Gauge(
            "web3_storage_direct_pins_size",
            "Size of direct pins in bytes",
        )
        self.psa_gauge = Gauge(
            "web3_storage_psa_pins_size",
            "Size of Pinning Services API pins in bytes",
        )
        self.total_gauge = Gauge(
            "web3_storage_total_pins_size",
            "Size of all pins in bytes",
        )

    def start(self):
        print("Starting exporter...")
        self.update()
        start_http_server(self.port, self.host)
        print(f"Started exporter on {self.host}:{self.port}")
        while True:
            self.update()
            sleep(600)

    def update(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        resp = requests.get("https://api.web3.storage/user/account", headers=headers)
        resp.raise_for_status()
        data = resp.json()
        direct = data["usedStorage"]["uploaded"]
        psa = data["usedStorage"]["psaPinned"]
        total = data["usedStorage"]["total"]
        self.direct_gauge.set(direct)
        self.psa_gauge.set(psa)
        self.total_gauge.set(total)
