# -*- coding: utf-8 -*-
"""UHC 极限生存冠军 (/hyp <玩家> uhc)"""
from ...utils import build_string, div, number_format


def run(cmd, p, rank, stats, args, footer):
    s = stats.get('UHC') or {}
    return build_string(cmd.msg('uhc.layout'), [
        rank + (p.get('displayname') or ''),
        number_format(s.get('score')),
        number_format(s.get('coins')),
        number_format(s.get('wins')),
        number_format(s.get('kills')),
        number_format(s.get('deaths')),
        div(s.get('kills'), s.get('deaths')),
    ])
