import os.path

def get_key():
    with open(os.path.join(os.path.dirname(__file__), ".env"), "r") as file:
        key = file.read().strip()
    return key