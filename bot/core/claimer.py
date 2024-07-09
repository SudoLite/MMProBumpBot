import asyncio
from time import time
from datetime import datetime
from urllib.parse import unquote
from datetime import timedelta
from random import randint

import aiohttp
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from pyrogram import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered
from pyrogram.raw.functions.messages import RequestWebView

from bot.config import settings
from bot.utils import logger
from bot.exceptions import InvalidSession
from .headers import headers


class Claimer:
    def __init__(self, tg_client: Client):
        self.session_name = tg_client.name
        self.tg_client = tg_client

    async def get_tg_web_data(self, proxy: str | None) -> str:
        if proxy:
            proxy = Proxy.from_str(proxy)
            proxy_dict = dict(
                scheme=proxy.protocol,
                hostname=proxy.host,
                port=proxy.port,
                username=proxy.login,
                password=proxy.password
            )
        else:
            proxy_dict = None

        self.tg_client.proxy = proxy_dict

        try:
            if not self.tg_client.is_connected:
                try:
                    await self.tg_client.connect()
                except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                    raise InvalidSession(self.session_name)

            web_view = await self.tg_client.invoke(RequestWebView(
                peer=await self.tg_client.resolve_peer('MMproBump_bot'),
                bot=await self.tg_client.resolve_peer('MMproBump_bot'),
                platform='android',
                from_bot_menu=False,
                url='https://mmbump.pro/'
            ))

            auth_url = web_view.url
            tg_web_data = unquote(
                string=unquote(
                    string=auth_url.split('tgWebAppData=', maxsplit=1)[1].split('&tgWebAppVersion', maxsplit=1)[0]))

            if self.tg_client.is_connected:
                await self.tg_client.disconnect()

            return tg_web_data

        except InvalidSession as error:
            raise error

        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error during Authorization: {error}")
            await asyncio.sleep(delay=3)

    async def login(self, http_client: aiohttp.ClientSession, tg_web_data: str) -> dict[str]:
        try:
            response = await http_client.post('https://api.mmbump.pro/v1/loginJwt', json={'initData': tg_web_data})
            response.raise_for_status()

            response_json = await response.json()

            return response_json['access_token']
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while getting Access Token: {error}")
            await asyncio.sleep(delay=3)

    async def get_farming_data(self, http_client: aiohttp.ClientSession) -> dict[str]:
        try:
            response = await http_client.get('https://api.mmbump.pro/v1/farming')
            response.raise_for_status()

            response_json = await response.json()

            return response_json
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when getting Profile Data: {error}")
            await asyncio.sleep(delay=3)

    async def buy_boost(self, http_client: aiohttp.ClientSession) -> dict[str]:
        try:
            response = await http_client.post('https://api.mmbump.pro/v1/product-list/buy', json={'id': settings.DEFAULT_BOOST})
            response.raise_for_status()

            response_json = await response.json()

            return response_json
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when buying boost: {error}")
            await asyncio.sleep(delay=3)

    async def claim_daily(self, http_client: aiohttp.ClientSession) -> dict[str]:
        try:
            response = await http_client.post('https://api.mmbump.pro/v1/grant-day/claim', json={})
            response.raise_for_status()

            response_json = await response.json()

            return response_json
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when claiming daily: {error}")
            await asyncio.sleep(delay=3)

    async def reset_daily(self, http_client: aiohttp.ClientSession) -> None:
        try:
            response = await http_client.post('https://api.mmbump.pro/v1/grant-day/reset', json={})
            response.raise_for_status()

            response_json = await response.json()

            return response_json
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when resetting daily reward: {error}")
            await asyncio.sleep(delay=3)

    async def get_tasks_list(self, http_client: aiohttp.ClientSession) -> dict[str]:
        try:
            response = await http_client.get('https://api.mmbump.pro/v1/task-list')
            response.raise_for_status()

            response_json = await response.json()

            return response_json
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when getting Tasks Data: {error}")
            await asyncio.sleep(delay=3)

    async def task_complete(self, http_client: aiohttp.ClientSession, task_id: str) -> str:
        try:
            response = await http_client.post('https://api.mmbump.pro/v1/task-list/complete', json={'id': task_id})
            response.raise_for_status()

            response_json = await response.json()

            return response_json
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while complete task: {error}")
            await asyncio.sleep(delay=3)

    async def start_farm(self, http_client: aiohttp.ClientSession, balance: int) -> None:
        try:
            response = await http_client.post('https://api.mmbump.pro/v1/farming/start', json={'status': "inProgress"})
            response.raise_for_status()

            resp = await response.json()
            status = resp['status']

            if status == "inProgress":
                logger.success(f"{self.session_name} | Successful Farming Started | "
                        f"Balance: <e>{balance}</e>")
                
                if settings.AUTO_CLAIM_MOON_BOUNS:
                    await asyncio.sleep(delay=randint(10, 25))
                    balance += settings.BASE_MOON_BOUNS
                    resp = await self.moon_claim(http_client=http_client, balance=balance)
                    if resp['balance']:
                        logger.success(f"{self.session_name} | Successful Moon bonus claimed | "
                                f"Balance: <e>{balance}</e> (<c>+{settings.BASE_MOON_BOUNS}</c>)")
            else:
                logger.warning(f"{self.session_name} | Can't start farming | Status: <r>{status}</r>")
                return

        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when Starting farm: {error}")
            await asyncio.sleep(delay=3)

    async def finish_farm(self, http_client: aiohttp.ClientSession, taps: int) -> dict[str]:
        try:
            response = await http_client.post('https://api.mmbump.pro/v1/farming/finish', json={'tapCount': taps})
            response.raise_for_status()

            response_json = await response.json()

            return response_json
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when Finishing farm: {error}")
            await asyncio.sleep(delay=3)

    async def moon_claim(self, http_client: aiohttp.ClientSession, balance: int) -> dict[str]:
        try:
            response = await http_client.post('https://api.mmbump.pro/v1/farming/moon-claim', json={'balance': balance})
            response.raise_for_status()

            response_json = await response.json()

            return response_json
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when Moon Claiming: {error}")
            await asyncio.sleep(delay=3)

    async def check_proxy(self, http_client: aiohttp.ClientSession, proxy: Proxy) -> None:
        try:
            response = await http_client.get(url='https://httpbin.org/ip', timeout=aiohttp.ClientTimeout(5))
            ip = (await response.json()).get('origin')
            logger.info(f"{self.session_name} | Proxy IP: {ip}")
        except Exception as error:
            logger.error(f"{self.session_name} | Proxy: {proxy} | Error: {error}")

    async def run(self, proxy: str | None) -> None:
        access_token_created_time = 0

        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None

        async with aiohttp.ClientSession(headers=headers, connector=proxy_conn) as http_client:
            if proxy:
                await self.check_proxy(http_client=http_client, proxy=proxy)

            while True:
                try:
                    if time() - access_token_created_time >= 3600:
                        tg_web_data = await self.get_tg_web_data(proxy=proxy)
                        access_token = await self.login(http_client=http_client, tg_web_data=tg_web_data)

                        http_client.headers["Authorization"] = f"Bearer {access_token}"

                        access_token_created_time = time()

                        farming_data = await self.get_farming_data(http_client=http_client)

                        day_grant_first = farming_data['day_grant_first']
                        day_grant_day = farming_data['day_grant_day']
                        system_time = farming_data['system_time']

                        if day_grant_first is None:
                            resp = await self.claim_daily(http_client=http_client)
                            if resp:
                                logger.success(f"{self.session_name} | Daily Reward Claimed! | New Balance: <e>{resp['balance']}</e> | Day: <g>{resp['day_grant_day']}</g>")
                        else:
                            next_claim_time = day_grant_first + timedelta(days=1).total_seconds() * day_grant_day
                            if next_claim_time < system_time:
                                if next_claim_time + timedelta(days=1).total_seconds() < system_time:
                                    await self.reset_daily(http_client=http_client)
                                    logger.info(f"{self.session_name} | Successful Reset Daily Reward")
                                    await asyncio.sleep(delay=5)

                                await self.claim_daily(http_client=http_client)

                        if settings.AUTO_CLAIM_TASKS:
                            await asyncio.sleep(delay=3)
                            tasks_data = await self.get_tasks_list(http_client=http_client)

                            for task in tasks_data:
                                if task['status'] == 'possible' and task['type'] == 'twitter':
                                    resp_task = await self.task_complete(http_client=http_client, task_id=task['id'])
                                    if resp_task['task']['status'] == 'granted':
                                        logger.success(f"{self.session_name} | Successful Claim Task | "
                                                    f"Task Title: <c>{task['name']}</c> | "
                                                    f"Task Reward: <g>+{task['grant']}</g>")
         
                    
                    
                    farming_data = await self.get_farming_data(http_client=http_client)

                    if settings.AUTO_BUY_BOOST is True:
                        if farming_data['info'].get('boost') is None or farming_data['info']['active_booster_finish_at'] < time():
                            boost_price = settings.BOOST_LEVLES[settings.DEFAULT_BOOST]
                            if boost_price > farming_data['balance']:
                                logger.warning(f"{self.session_name} | Can't buy boost, not enough money | Balance: <e>{balance}</e> "
                                            f"| Boost price: <r>{boost_price}</r>")
                            else:
                                await asyncio.sleep(delay=randint(3, 5))
                                resp = await self.buy_boost(http_client=http_client)
                                if resp:
                                    logger.success(f"{self.session_name} | Successful Bought boost <m>{resp['id']}</m> | Balance: <e>{resp['balance']}</e>")

                    balance = farming_data['balance']

                    logger.info(f"{self.session_name} | Balance: <e>{farming_data['balance']}</e>")

                    farm_status = farming_data['session']['status']

                    if farm_status == "await":
                        await self.start_farm(http_client=http_client, balance=balance)

                    elif farm_status == "inProgress":
                        moon_time = farming_data['session']['moon_time']
                        start_at = farming_data['session']['start_at']
                        finish_at = start_at + settings.BASE_FARM_TIME
                        time_left = finish_at - time()

                        if time_left < 0:
                            taps = randint(settings.TAPS_COUNT[0], settings.TAPS_COUNT[1])
                            boost = farming_data['info'].get('boost')

                            if boost is not None:
                                taps *= int(boost.split("x")[1])

                            resp = await self.finish_farm(http_client=http_client, taps=taps)
                            if resp:
                                amount = int(resp['session']['amount']) + int(resp['session']['taps'])
                                logger.success(f"{self.session_name} | Successful MFinished farming | "
                                            f"Balance: <e>{resp['balance']}</e> (<c>+{amount}</c>)")
                                            
                                await asyncio.sleep(delay=randint(3, 5))
                                await self.start_farm(http_client=http_client, balance=resp['balance'])

                        else:
                            logger.info(f"{self.session_name} | Farming in progress, <m>{round(time_left / 60, 1)}</m> mins to end")

                                    

                except InvalidSession as error:
                    raise error

                except Exception as error:
                    logger.error(f"{self.session_name} | Unknown error: {error}")
                    await asyncio.sleep(delay=3)

                else:
                    sleep = randint(settings.SLEEP_BETWEEN_CLAIM[0], settings.SLEEP_BETWEEN_CLAIM[1])
                    logger.info(f"{self.session_name} | Sleep {sleep} seconds")
                    await asyncio.sleep(delay=sleep)


async def run_claimer(tg_client: Client, proxy: str | None):
    try:
        await Claimer(tg_client=tg_client).run(proxy=proxy)
    except InvalidSession:
        logger.error(f"{tg_client.name} | Invalid Session")
