import functools
import socket
from typing import Callable
import asyncio
from aioping import ping
from app.config.config import config
from .tg_notification import send_all_users
from ..config.config import logger
from ..models.host import Host


async def ping_host(host: str, max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """

    :param host: ip или хост ресурса
    :param max_attempts: максимальное количество попыток
    :param delay: начальная задержка между попытками (секунды)
    :param backoff: множитель для увеличения задержки
    :return:
    """
    for attempt in range(1, max_attempts + 1):
        if attempt > 1:
            logger.info(f"Попытка {attempt}/{max_attempts} для `{host}`")
        try:
            return await ping(host)
        except socket.gaierror as exp:

            logger.error(f"Имя узла или имя службы `{host}` не указано или неизвестно")
            raise ValueError(f"Имя узла или имя службы `{host}` не указано или неизвестно")
        except TimeoutError as exp:
            logger.error(f'Хост `{host}` недоступен')
        finally:
            if attempt == max_attempts:
                logger.error(f"Все {max_attempts} попытки для `{host}` завершились ошибками")
                raise TimeoutError(f"Хост `{host}` недоступен")
            wait_time = delay * (backoff ** (attempt - 1))
            await asyncio.sleep(wait_time)
    return None


async def ping_all_hosts(hosts: list[Host]):
    task_to_host = {}
    tasks = []
    for host in hosts:
        task = asyncio.create_task(ping_host(host.address))
        tasks.append(task)
        task_to_host[task] = host
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for task, result in zip(tasks, results):
        host = task_to_host[task]
        if isinstance(result, ValueError):
            if host.status:
                host.status = False
                config.HOSTS.edit_host(host)
                await send_all_users(
                    f"Для хоста *{host.name}* имя узла или имя службы *{host.address}* не указано или неизвестно 🔴")

        elif isinstance(result, TimeoutError):
            if host.status:
                host.status = False
                config.HOSTS.edit_host(host)
                await send_all_users(f"Хост *{host.name}* недоступен 🔴")
        else:
            if not host.status:
                host.status = True
                await send_all_users(f"Хост *{host.name}* снова доступен 🟢")
                config.HOSTS.edit_host(host)
