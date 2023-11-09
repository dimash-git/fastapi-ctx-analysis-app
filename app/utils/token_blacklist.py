from typing import Set

BLACKLIST_FILE = "cache/blacklist_tokens.txt"


def load_blacklist() -> Set[str]:
    try:
        with open(BLACKLIST_FILE, "r") as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()


def is_token_blacklisted(token: str) -> bool:
    blacklisted_tokens = load_blacklist()
    return token in blacklisted_tokens


def blacklist_token(token: str):
    with open(BLACKLIST_FILE, "a") as file:
        file.write(token + "\n")
