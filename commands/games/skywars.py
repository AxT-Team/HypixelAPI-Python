# -*- coding: utf-8 -*-
"""空岛战争 (/hyp <玩家> sw)"""
from ...utils import build_string, div, number_format, plain_string


def run(cmd, p, rank, stats, args, footer):
    s = stats.get('SkyWars') or {}
    return build_string(cmd.msg('sw.layout'), [
        rank + (p.get('displayname') or ''),
        plain_string(s.get('levelFormatted')) or '1',
        number_format(s.get('coins')),
        number_format(s.get('assists')),
        number_format(s.get('kills')),
        number_format(s.get('deaths')),
        div(s.get('kills'), s.get('deaths')),
        number_format(s.get('wins')),
        number_format(s.get('losses')),
        div(s.get('wins'), s.get('losses')),
    ])
