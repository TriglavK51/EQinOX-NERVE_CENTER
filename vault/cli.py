"""Command-line interface for the local encrypted vault."""

from __future__ import annotations

import argparse

from vault.vault import Vault


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("set", "get", "delete"))
    parser.add_argument("name")
    parser.add_argument("value", nargs="?")
    parser.add_argument("--passphrase")
    args = parser.parse_args()
    vault = Vault(args.passphrase)
    if args.action == "set":
        if args.value is None:
            parser.error("set requires VALUE")
        vault.set(args.name, args.value)
    elif args.action == "get":
        print(vault.get(args.name))
    else:
        vault.delete(args.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
