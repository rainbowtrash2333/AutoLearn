from typing import Optional, Callable, Any, Union
from functools import wraps
import aiohttp
import asyncio

class RequestError(Exception):
    """自定义请求异常基类"""

    def __init__(self, message: str, url: Optional[str] = None, status_code: Optional[int] = None):
        self.message = message
        self.url = url
        self.status_code = status_code
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} (URL: {self.url}, Status: {self.status_code})"


class Non200Error(RequestError):
    """非200状态码异常"""
    pass


class RetryExhaustedError(RequestError):
    """重试次数耗尽异常"""
    pass


DEFAULT_RETRIES = 5
DEFAULT_TIMEOUT = 10  # 默认超时时间

DEFAULT_HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0",
    "X-Requested-With": "XMLHttpRequest",
    "isapp": "0",
    "sec-ch-ua": '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}


def retry(
        max_retries: int = DEFAULT_RETRIES,
        allowed_methods: tuple = ("GET", "POST"),
        handled_status_codes: tuple = (500, 502, 503, 504),
        handled_exceptions: tuple = (aiohttp.ClientConnectionError, aiohttp.ClientResponseError, asyncio.TimeoutError)
) -> Callable:
    """
    异步请求重试装饰器

    :param max_retries: 最大重试次数
    :param allowed_methods: 需要重试的HTTP方法
    :param handled_status_codes: 需要重试的状态码
    :param handled_exceptions: 需要重试的异常类型
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> aiohttp.ClientResponse:
            last_exception = None
            response = None

            for attempt in range(max_retries + 1):
                try:
                    response = await func(*args, **kwargs)

                    # 检查状态码
                    if response.status != 200:
                        if response.status in handled_status_codes:
                            raise Non200Error(
                                f"Invalid status code: {response.status}",
                                url=response.url,
                                status_code=response.status
                            )
                        else:
                            return response  # 返回非200但不在处理列表中的响应

                    return response

                except handled_exceptions as e:
                    last_exception = e
                    if attempt == max_retries:
                        break
                    continue

                except Exception as e:
                    raise RequestError(
                        f"Unhandled exception occurred: {str(e)}",
                        url=str(getattr(response, 'url', None)),
                        status_code=getattr(response, 'status', None)
                    ) from e

            raise RetryExhaustedError(
                f"Max retries ({max_retries}) exceeded",
                url=str(getattr(response, 'url', None)),
                status_code=getattr(response, 'status', None)
            ) from last_exception

        return wrapper

    return decorator


@retry()
async def get(
        url: str,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: float = DEFAULT_TIMEOUT
) -> aiohttp.ClientResponse:
    """
    带重试功能的异步GET请求

    :param url: 请求URL
    :param headers: 请求头，默认使用DEFAULT_HEADERS
    :param params: 查询参数
    :param timeout: 超时时间（秒）
    """
    final_headers = DEFAULT_HEADERS.copy()
    if headers:
        final_headers.update(headers)

    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            headers=final_headers,
            params=params,
            timeout=aiohttp.ClientTimeout(total=timeout)
        ) as response:
            return response


@retry()
async def post(
        url: str,
        data: Optional[dict] = None,
        headers: Optional[dict] = None,
        json: Optional[dict] = None,
        timeout: float = DEFAULT_TIMEOUT
) -> aiohttp.ClientResponse:
    """
    带重试功能的异步POST请求

    :param url: 请求URL
    :param data: 表单数据
    :param headers: 请求头，默认使用DEFAULT_HEADERS
    :param json: JSON数据
    :param timeout: 超时时间（秒）
    """
    final_headers = DEFAULT_HEADERS.copy()
    if headers:
        final_headers.update(headers)

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
            headers=final_headers,
            data=data,
            json=json,
            timeout=aiohttp.ClientTimeout(total=timeout)
        ) as response:
            return response