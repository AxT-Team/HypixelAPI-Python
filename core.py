# -*- coding: utf-8 -*-
"""HypixelCheck 核心: 命令注册 / 冷却 / 资源加载"""
import json
import os
import time

from .commands.hypixel import HypixelCommand

VERSION = '2.0.0'

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG = os.path.join(_BASE_DIR, 'config.json')
RESOURCE_DIR = os.path.join(_BASE_DIR, 'resources')


class HypixelCheck:
    """对外主入口:

        checker = HypixelCheck()
        text = checker.execute('/hyp playerName zb aa', userId)
    """

    def __init__(self, config_file=DEFAULT_CONFIG):
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        self.resources = {}
        self.staffs = [str(x) for x in config.get('staffs', [])]
        self.cooldown = config.get('cooldown', 10)
        self.cooldown_message = config.get('cooldown_message', '获取速度太快了啦!')
        self.user_last_executions = {}
        self.commands = [
            HypixelCommand(self, config.get('hypixel', {})),
        ]

    def load_json_resource(self, filename):
        path = os.path.join(RESOURCE_DIR, filename)
        if not os.path.isfile(path):
            return False
        with open(path, 'r', encoding='utf-8') as f:
            self.resources[filename] = json.load(f)
        return True

    def get_json_value(self, filename, path):
        cur = self.resources.get(filename)
        for key in path.split('.'):
            if isinstance(cur, dict) and key in cur:
                cur = cur[key]
            else:
                return None
        return cur

    def execute(self, text, user):
        """执行一条命令, 返回字符串结果; 未匹配任何命令时返回 None"""
        user = str(user)
        args = [x for x in str(text).lower().split(' ') if x]
        if not args:
            return None
        for command in self.commands:
            if args[0] in command.get_name():
                if (command.has_cooldown()
                        and user not in self.staffs
                        and user in self.user_last_executions
                        and time.time() - self.user_last_executions[user] < self.cooldown):
                    return self.cooldown_message
                self.user_last_executions[user] = time.time()
                try:
                    return command.execute(args, user in self.staffs)
                except Exception as e:  # 防御性兜底, 避免异常直接抛给调用方
                    import logging
                    logging.getLogger('hypixelcheck').exception('command failed: %s', text)
                    return '查询过程中发生内部错误: {}'.format(type(e).__name__)
        return None
