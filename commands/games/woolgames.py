# -*- coding: utf-8 -*-
"""羊毛游戏 WoolGames (/hyp <玩家> ww) - 最新 API 新增游戏"""
from ...utils import build_string, div, json_get, number_format


def _level(exp):
    """官方等级公式: 前 4 级每级 1000/2000/3000/4000 exp, 之后每级 5000 exp"""
    level = 0.0
    remaining = float(exp or 0)
    for need in (1000, 2000, 3000, 4000):
        if remaining < need:
            return level + remaining / need
        remaining -= need
        level += 1
    while remaining >= 5000:
        remaining -= 5000
        level += 1
    return level + remaining / 5000


def run(cmd, p, rank, stats, args, footer):
    s = stats.get('WoolGames') or {}
    ww = json_get(s, 'wool_wars.stats', {}) or {}
    sheep = json_get(s, 'sheep_wars.stats', {}) or {}
    ctw = json_get(s, 'capture_the_wool.stats', {}) or {}
    losses = (ww.get('games_played') or 0) - (ww.get('wins') or 0)
    return build_string(cmd.msg('ww.layout'), [
        rank + (p.get('displayname') or ''),
        _level(json_get(s, 'progression.experience', 0)),
        number_format(s.get('coins')),
        number_format(ww.get('games_played')),
        number_format(ww.get('wins')),
        number_format(losses),
        div(ww.get('wins'), losses),
        number_format(ww.get('kills')),
        number_format(ww.get('deaths')),
        div(ww.get('kills'), ww.get('deaths')),
        number_format(ww.get('assists')),
        number_format(ww.get('wool_placed')),
        number_format(sheep.get('wins')),
        number_format(sheep.get('kills')),
        number_format(ctw.get('participated_wins')),
        number_format(ctw.get('wools_captured')),
    ])
