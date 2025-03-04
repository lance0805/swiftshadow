from typing import Literal

from requests import get

from swiftshadow.helpers import plaintextToProxies
from swiftshadow.models import Provider, Proxy
from swiftshadow.types import MonosansProxyDict
from swiftshadow.validator import validate_proxies


async def Monosans(
    countries: list[str] = [],
    protocol: Literal["http", "https", "socks5"] = "http",
) -> list[Proxy]:
    response = get(
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies.json"
    )
    proxy_dicts: list[MonosansProxyDict] = response.json()
    proxies_to_validate: list[Proxy] = []
    for proxy_dict in proxy_dicts:
        if proxy_dict["protocol"] != protocol:
            continue
        if (
            len(countries) != 0
            and proxy_dict["geolocation"]["country"]["iso_code"] not in countries
        ):
            continue
        proxy = Proxy(
            ip=proxy_dict["host"],
            port=proxy_dict["port"],
            protocol=proxy_dict["protocol"],
        )
        proxies_to_validate.append(proxy)
    result = await validate_proxies(proxies_to_validate)
    return result


async def Thespeedx(
    countries: list[str] = [], protocol: Literal["http", "https", "socks5"] = "http"
):
    raw: str = get(
        f"https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/{protocol}.txt"
    ).text
    proxies: list[Proxy] = plaintextToProxies(raw, protocol=protocol)
    results = await validate_proxies(proxies)
    return results


async def ProxyScrape(
    countries: list[str] = [], protocol: Literal["http", "https", "socks5"] = "http"
):
    baseUrl = f"https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol={protocol}&proxy_format=ipport&format=json"
    proxies: list[Proxy] = []
    if len(countries) == 0:
        apiUrl = baseUrl + "&country=all"
    else:
        apiUrl = baseUrl + "&country=" + ",".join([i.upper() for i in countries])
    raw = get(apiUrl).json()
    for ipRaw in raw["proxies"]:
        proxy = Proxy(protocol=protocol, ip=ipRaw["ip"], port=ipRaw["port"])
        proxies.append(proxy)
    results = await validate_proxies(proxies)
    return results


async def GoodProxy(
    countries: list[str] = [], protocol: Literal["http", "https", "socks5"] = "http"
):
    baseUrl = "https://raw.githubusercontent.com/yuceltoluyag/GoodProxy/refs/heads/main/GoodProxy.txt"
    proxies: list[Proxy] = []
    raw = get(baseUrl).text

    for line in raw.splitlines():
        if line == "":
            continue
        line = line.split("|")[0].split(":")
        proxy = Proxy(ip=line[0], port=int(line[1]), protocol=protocol)
        proxies.append(proxy)
    results = await validate_proxies(proxies)
    return results


async def OpenProxyList(
    countries: list[str] = [], protocol: Literal["http", "https", "socks5"] = "http"
):
    raw = get(f"https://api.openproxylist.xyz/{protocol}.txt").text
    proxies: list[Proxy] = plaintextToProxies(raw, protocol=protocol)
    results = await validate_proxies(proxies)
    return results


async def MuRongPIG(
    countries: list[str] = [], protocol: Literal["http", "https", "socks5"] = "http"
):
    raw = get(
        f"https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/refs/heads/main/{protocol}_checked.txt"
    ).text
    proxies: list[Proxy] = plaintextToProxies(raw, protocol=protocol)
    results = await validate_proxies(proxies)
    return results


async def KangProxy(
    countries: list[str] = [], protocol: Literal["http", "https", "socks5"] = "http"
):
    raw = get(
        f"https://github.com/officialputuid/KangProxy/raw/refs/heads/KangProxy/{protocol}/{protocol}.txt"
    ).text
    proxies: list[Proxy] = plaintextToProxies(raw, protocol=protocol)
    results = await validate_proxies(proxies)
    return results


async def Mmpx12(
    countries: list[str] = [], protocol: Literal["http", "https", "socks5"] = "http"
):
    raw = get(
        f"https://github.com/mmpx12/proxy-list/raw/refs/heads/master/{protocol}.txt"
    ).text
    proxies: list[Proxy] = plaintextToProxies(raw, protocol=protocol)
    results = await validate_proxies(proxies)
    return results


async def Anonym0usWork1221(
    countries: list[str] = [], protocol: Literal["http", "https", "socks5"] = "http"
):
    raw = get(
        f"https://github.com/Anonym0usWork1221/Free-Proxies/raw/refs/heads/main/proxy_files/{protocol}_proxies.txt"
    ).text
    proxies: list[Proxy] = plaintextToProxies(raw, protocol=protocol)
    results = await validate_proxies(proxies)
    return results


async def ProxySpace(
    countries: list[str] = [], protocol: Literal["http", "https", "socks5"] = "http"
):
    raw = get(f"https://proxyspace.pro/{protocol}.txt").text
    proxies: list[Proxy] = plaintextToProxies(raw, protocol=protocol)
    results = await validate_proxies(proxies)
    return results


Providers: list[Provider] = [
    Provider(
        providerFunction=ProxyScrape, countryFilter=True, protocols=["http", "socks5"]
    ),
    Provider(
        providerFunction=Monosans, countryFilter=True, protocols=["http", "socks5"]
    ),
    Provider(
        providerFunction=MuRongPIG, countryFilter=False, protocols=["http", "socks5"]
    ),
    Provider(
        providerFunction=Thespeedx, countryFilter=False, protocols=["http", "socks5"]
    ),
    Provider(
        providerFunction=Anonym0usWork1221,
        countryFilter=False,
        protocols=["http", "https", "socks5"],
    ),
    Provider(
        providerFunction=Mmpx12,
        countryFilter=False,
        protocols=["http", "https", "socks5"],
    ),
    Provider(
        providerFunction=GoodProxy, countryFilter=False, protocols=["http", "socks5"]
    ),
    Provider(
        providerFunction=KangProxy,
        countryFilter=False,
        protocols=["http", "https", "socks5"],
    ),
    Provider(
        providerFunction=ProxySpace, countryFilter=False, protocols=["http", "socks5"]
    ),
    Provider(
        providerFunction=OpenProxyList,
        countryFilter=False,
        protocols=["http", "socks5"],
    ),
]
