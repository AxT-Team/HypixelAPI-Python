# -*- coding: utf-8 -*-
"""HypixelCheck Python 重构版

用法:
    from hypixelcheck import HypixelCheck
    checker = HypixelCheck()          # 使用包内 config.json
    text = checker.execute('/hyp 玩家名 zb aa', userId)

或异步 (供 aiohttp/asyncio 环境):
    text = await checker.execute_async('/hyp 玩家名 bw', userId)
"""
import asyncio

from .core import HypixelCheck as _HypixelCheck, VERSION

__all__ = ['HypixelCheck', 'VERSION']


class HypixelCheck(_HypixelCheck):
    async def execute_async(self, text, user):
        return await asyncio.get_event_loop().run_in_executor(
            None, self.execute, text, user)
