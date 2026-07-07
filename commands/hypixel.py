# -*- coding: utf-8 -*-
"""/hyp 命令调度器: 解析玩家与分类, 分发到 games/ 下的各游戏模块"""
import os

from ..api import HypixelAPI
from ..utils import CACHE_DIRECTORY, build_string, size_format
from .games import (
    general, guild, bedwars, skywars, duels, uhc, megawalls, blitz,
    buildbattle, woolgames, murdermystery, zombies, skyblock, pit,
    recent, parkour,
)


class HypixelCommand:
    def __init__(self, core, config):
        self.core = core
        self.config = config
        self.resource = config.get('resource', 'hypixel.json')
        self.api = HypixelAPI(config['api_key'])
        core.load_json_resource(self.resource)

        self.handlers = {}
        for module, names in [
            (guild, ['guild', 'g']),
            (blitz, ['blitzsg', 'bsg', 'hungergames']),
            (duels, ['duels', 'duel']),
            (uhc, ['uhc']),
            (megawalls, ['megawalls', 'mw']),
            (skywars, ['skywars', 'sw']),
            (buildbattle, ['buildbattle', 'bb']),
            (woolgames, ['woolgames', 'woolwars', 'ww']),
            (bedwars, ['bedwars', 'bw']),
            (murdermystery, ['murdermystery', 'mm']),
            (zombies, ['zombies', 'zb']),
            (skyblock, ['skyblock', 'sb']),
            (pit, ['pit', 'thepit']),
            (recent, ['recent', 'r']),
            (parkour, ['parkour', 'p']),
            (general, ['general']),
        ]:
            for name in names:
                self.handlers[name] = module.run

    def get_name(self):
        return ['/hypixel', '/hyp']

    def has_cooldown(self):
        return True

    def get_usage(self):
        return build_string(self.core.get_json_value(self.resource, 'usage'))

    def msg(self, key):
        return self.core.get_json_value(self.resource, 'messages.' + key)

    @property
    def timezone_offset(self):
        return self.config.get('timezone_offset', 0)

    def fetch_player(self, name):
        result, status = self.api.player_by_name(name)
        if status == 429:
            return None, self.msg('info.rate_limit_reached')
        if result is None:
            return None, self.msg('info.request_failed' if status == 0 else 'info.incomplete_json')
        if not result.get('success'):
            return None, self.msg('info.incomplete_json')
        if not result.get('player'):
            return None, self.msg('info.player_not_found')
        return result['player'], None

    def cache_command(self, action):
        files = []
        if os.path.isdir(CACHE_DIRECTORY):
            files = [os.path.join(CACHE_DIRECTORY, f)
                     for f in os.listdir(CACHE_DIRECTORY)
                     if os.path.isfile(os.path.join(CACHE_DIRECTORY, f))]
        total = sum(os.path.getsize(f) for f in files)
        if action == 'stats':
            return build_string(self.msg('cache.stats'), [
                len(self.core.user_last_executions), len(files), size_format(total)])
        if action == 'clean':
            for f in files:
                os.remove(f)
            return build_string(self.msg('cache.clean'), [size_format(total)])
        return build_string(self.msg('cache.usage'))

    @staticmethod
    def rank_prefix(p):
        if p.get('rank') and p['rank'] not in ('NONE', 'NORMAL'):
            return '[' + p['rank'] + '] '
        if p.get('monthlyPackageRank') and p['monthlyPackageRank'] != 'NONE':
            return '[MVP++] '
        if p.get('newPackageRank') and p['newPackageRank'] != 'NONE':
            return '[' + p['newPackageRank'].replace('_PLUS', '+') + '] '
        return ''

    def execute(self, args, is_staff=False):
        if len(args) < 2 or not args[1]:
            return self.get_usage()

        if args[1] == 'cache':
            return self.cache_command(args[2] if len(args) > 2 else 'stats')

        p, err = self.fetch_player(args[1])
        if err:
            return err

        category = args[2] if len(args) > 2 else 'general'
        handler = self.handlers.get(category)
        if handler is None:
            return self.get_usage()

        rank = self.rank_prefix(p)
        stats = p.get('stats') or {}
        footer = build_string(self.msg('info.learn_more') or '', [''])
        return handler(self, p, rank, stats, args, footer)
