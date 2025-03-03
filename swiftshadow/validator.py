import asyncio
import re

import aiohttp
from aiohttp_socks import ProxyConnector

from swiftshadow.models import Proxy


def find_ipv4_in_string(input_string: str) -> str | None:
    """
    Extract IPv4 Address from input and return the same.

    Args:
        input_string: Input string

    Returns:
        ipv4_address: If found
    """
    ipv4_pattern = r"\b((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\b"

    match = re.search(ipv4_pattern, input_string)

    if match:
        return match.group(0)
    else:
        return None


async def get_host_ip(async_session: aiohttp.ClientSession) -> str | None:
    """
    Gets the hosts external IP for validation.

    Args:
        async_session: AioHTTP client session object

    Returns:
        text: Host IP
    """
    async with async_session.get("https://ifconfig.me") as response:
        text = await response.text()
        ip = find_ipv4_in_string(text)
        return ip


async def check_proxy(async_session: aiohttp.ClientSession, proxy: Proxy) -> str:
    """
    Check one proxy object.

    Args:
        async_session: aiohttp client session object
        proxy: Proxy Object

    Returns:
        text: API response text
    """
    proxy_url = proxy.as_string()
    if proxy_url.startswith('socks'):
        # 使用 aiohttp_socks 处理 SOCKS 代理
        connector = ProxyConnector.from_url(proxy_url)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(
                url="https://google.com",
                timeout=4,
            ) as response:
                text = await response.text()
                return text
    else:
        # 原有的 HTTP/HTTPS 代理处理逻辑
        async with async_session.get(
            url="https://google.com",
            proxy=proxy_url,
            timeout=4,
        ) as response:
            text = await response.text()
            return text


async def validate_proxies(proxies: list[Proxy]) -> list[Proxy]:
    """
    Validate all proxies asynchronously.

    Args:
        proxies: List of Proxy objects

    Returns:
        working_proxies: List of working Proxies
    """
    working_proxies: list[Proxy] = []
    async with aiohttp.ClientSession() as async_session:
        tasks = []

        host_task = asyncio.create_task(coro=get_host_ip(async_session))
        tasks.append(host_task)

        for proxy in proxies:
            task = asyncio.create_task(coro=check_proxy(async_session, proxy))
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)
        host_ip = results[0]
        results = results[1:]

        for proxy, result in zip(proxies, results):
            if type(result) is not str:
                continue
            result_ip = find_ipv4_in_string(result)
            if result_ip and result_ip != host_ip:
                working_proxies.append(proxy)
    return working_proxies
