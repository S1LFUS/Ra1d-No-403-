import os
from hmac import new
from typing import Union
from hashlib import sha1
from base64 import b64encode


def device_id(data: bytes = None) -> str:
    if isinstance(data, str): data = bytes(data, 'utf-8')
    identifier = bytes.fromhex("42") + (data or os.urandom(20))
    mac = new(bytes.fromhex("02B258C63559D8804321C5D5065AF320358D366F"), identifier, sha1)
    return f"{identifier.hex()}{mac.hexdigest()}".upper()


def signature(data: Union[str, bytes]) -> str:
    data = data if isinstance(data, bytes) else data.encode("utf-8")
    return b64encode(bytes.fromhex("42") + new(bytes.fromhex("F8E7A61AC3F725941E3AC7CAE2D688BE97F30B93"), data, sha1).digest()).decode("utf-8")
