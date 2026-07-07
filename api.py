# -*- coding: utf-8 -*-
"""Hypixel API v2 客户端 (https://api.hypixel.net, API-Key 请求头认证)"""
import json

from .utils import get_url

API_BASE_URL = 'https://api.hypixel.net/v2'


class HypixelAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get(self, endpoint, params=None, cache=300):
        """请求 API, 返回 (dict|None, http_status)"""
        query = dict(params or {})
        query['key'] = self.api_key
        body, status = get_url(API_BASE_URL + endpoint, query, cache)
        if not body:
            return None, status
        try:
            return json.loads(body), status
        except ValueError:
            return None, status

    def player_by_name(self, name):
        return self.get('/player', {'name': name})

    def guild_by_player(self, uuid):
        return self.get('/guild', {'player': uuid})

    def status(self, uuid):
        return self.get('/status', {'uuid': uuid}, cache=10)

    def recent_games(self, uuid):
        return self.get('/recentgames', {'uuid': uuid}, cache=45)

    def skyblock_profile(self, profile_id):
        return self.get('/skyblock/profile', {'profile': profile_id})

    def skyblock_auction(self, profile_id):
        return self.get('/skyblock/auction', {'profile': profile_id})
