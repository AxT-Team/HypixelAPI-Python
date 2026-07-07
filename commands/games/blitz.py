# -*- coding: utf-8 -*-
"""闪电饥饿游戏 (/hyp <玩家> bsg)"""
from ...utils import build_string, div, number_format


def run(cmd, p, rank, stats, args, footer):
    s = stats.get('HungerGames') or {}
    return build_string(cmd.msg('bsg.layout'), [
        rank + (p.get('displayname') or ''),
        number_format(s.get('games_played')),
        number_format(s.get('coins')),
        number_format(s.get('chests_opened')),
        number_format(s.get('kills')),
        number_format(s.get('deaths')),
        div(s.get('kills'), s.get('deaths')),
    ])
