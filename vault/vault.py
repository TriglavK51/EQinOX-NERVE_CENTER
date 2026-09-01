"""AES-GCM vault with a key derived at runtime from a supplied passphrase."""

from __future__ import annotations

import base64
import json
import os
import secrets
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

from core.utils import project_path

VAULT_PATH = project_path("state", "vault.json")


class Vault:
    def __init__(self, passphrase: str | None = None, path: Path = VAULT_PATH) -> None:
        self.passphrase = passphrase or os.environ.get("NERVE_CENTER_VAULT_PASSPHRASE")
        if not self.passphrase:
            raise ValueError(
                "vault passphrase must be supplied via argument or NERVE_CENTER_VAULT_PASSPHRASE"
            )
        self.path = path

    def _load(self) -> dict[str, object]:
        if not self.path.exists():
            return {"salt": base64.b64encode(secrets.token_bytes(16)).decode(), "items": {}}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _key(self, salt: str) -> bytes:
        return Scrypt(salt=base64.b64decode(salt), length=32, n=2**14, r=8, p=1).derive(
            self.passphrase.encode()
        )

    def set(self, name: str, value: str) -> None:
        if not name or not isinstance(value, str):
            raise ValueError("name and value are required")
        document = self._load()
        nonce = secrets.token_bytes(12)
        encrypted = AESGCM(self._key(str(document["salt"]))).encrypt(
            nonce, value.encode(), name.encode()
        )
        document["items"][name] = base64.b64encode(nonce + encrypted).decode()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(document, sort_keys=True), encoding="utf-8")

    def get(self, name: str) -> str:
        document = self._load()
        encoded = document["items"].get(name)
        if not encoded:
            raise KeyError(name)
        raw = base64.b64decode(encoded)
        return (
            AESGCM(self._key(str(document["salt"])))
            .decrypt(raw[:12], raw[12:], name.encode())
            .decode()
        )

    def delete(self, name: str) -> None:
        document = self._load()
        document["items"].pop(name, None)
        self.path.write_text(json.dumps(document, sort_keys=True), encoding="utf-8")
