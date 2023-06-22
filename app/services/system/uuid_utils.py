import uuid


def get_uuid():
    random_uuid = uuid.uuid4()
    return random_uuid.hex
