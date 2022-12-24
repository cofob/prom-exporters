from os import environ
from .exporter import Web3StorageExporter


if __name__ == "__main__":
    token = environ["WEB3_STORAGE_TOKEN"]
    port = int(environ.get("WEB3_STORAGE_PORT", 9325))
    host = environ.get("WEB3_STORAGE_HOST", "0.0.0.0")
    exporter = Web3StorageExporter(token, port, host)
    exporter.start()
