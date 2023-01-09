import re


def is_valid_email(email: str):
    return re.search(
        "^[a-zA-Z0-9_\.]+@([a-zA-Z0-9]+\.)+[a-zA-Z0-9]{2,4}$", email)
