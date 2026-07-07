# -*- coding: utf-8 -*-
"""超级战墙 (/hyp <玩家> mw)"""
from ...utils import build_string, div, number_format


def run(cmd, p, rank, stats, args, footer):
    s = stats.get('Walls3') or {}
    return build_string(cmd.msg('mw.layout'), [
        rank + (p.get('displayname') or ''),
        number_format(s.get('wither_damage')),
        s.get('chosen_class') or '无',
        number_format(s.get('coins')),
        number_format(s.get('kills')),
        number_format(s.get('assists')),
        number_format(s.get('deaths')),
        div(s.get('kills'), s.get('deaths')),
        number_format(s.get('final_kills')),
        number_format(s.get('final_assists')),
        number_format(s.get('final_deaths')),
        div(s.get('final_kills'), s.get('final_deaths')),
        number_format(s.get('wins')),
        number_format(s.get('losses')),
        div(s.get('wins'), s.get('losses')),
    ])
