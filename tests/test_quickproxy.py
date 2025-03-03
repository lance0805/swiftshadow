from swiftshadow import QuickProxy
from swiftshadow.models import Proxy


def test_quickProxy():
    proxy = QuickProxy(protocol="socks5")
    assert isinstance(proxy, Proxy)
