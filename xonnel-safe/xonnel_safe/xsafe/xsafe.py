from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...

import getpass

import keyring


class XSafe:
    def __init__(self, service: str = "xonnel"):
        self.service = str(service)

    def set(self, key: str, value: str):
        if key is None or str(key).strip() == "":
            raise ValueError("key cannot be empty")
        if value is None:
            raise ValueError("value cannot be None")

        keyring.set_password(self.service, str(key), str(value))
        return value

    def get(self, key: str, default=None):
        if key is None or str(key).strip() == "":
            raise ValueError("key cannot be empty")

        value = keyring.get_password(self.service, str(key))
        if value is None:
            return default
        return value

    def has(self, key: str) -> bool:
        return self.get(key) is not None

    def delete(self, key: str) -> bool:
        if key is None or str(key).strip() == "":
            raise ValueError("key cannot be empty")

        try:
            keyring.delete_password(self.service, str(key))
            return True
        except Exception:
            return False

    def require(self, key: str, prompt: str | None = None) -> str:
        value = self.get(key)
        if value is not None:
            return value

        txt = prompt or f"Enter secret for [{self.service}:{key}]: "
        value = getpass.getpass(txt)
        self.set(key, value)
        return value


def test():
    safe = XSafe(service="xonnel-mail")

    # first time: asks and stores
    password = safe.require("smtp_password", prompt="SMTP password: ")

    # later: loads from Windows credential storage
    print("Loaded:", "*" * len(password))

    # examples
    safe.set("smtp_user", "name@example.com")
    print("user:", safe.get("smtp_user"))
    print("has smtp_password:", safe.has("smtp_password"))


if __name__ == "__main__":
    test()