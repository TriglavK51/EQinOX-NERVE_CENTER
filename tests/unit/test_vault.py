from vault.vault import Vault


def test_vault_round_trip(tmp_path) -> None:
    vault = Vault("test-passphrase", tmp_path / "vault.json")
    vault.set("sample", "secret")
    assert vault.get("sample") == "secret"
