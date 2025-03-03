from datetime import datetime
from typing import Literal


from swiftshadow.models import Proxy


def log(level, message):
    level = level.upper()
    print(
        f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - [swiftshadow] - {level} : {message}"
    )


def plaintextToProxies(
    text: str, protocol: Literal["http", "https", "socks5"]
) -> list[Proxy]:
    proxies: list[Proxy] = []
    for line in text.splitlines():
        try:
            ip, port = line.split(":")
        except ValueError:
            continue
        proxy = Proxy(ip=ip, port=int(port), protocol=protocol)
        proxies.append(proxy)
    return proxies
