# -*- coding: utf-8 -*-
"""天坑乱斗 The Pit (/hyp <玩家> pit)"""
from ...utils import build_string, div, number_format

EXP_PHASED = [15, 30, 50, 75, 125, 300, 600, 800, 900, 1000, 1200, 1500]
PRESTIGE_MULT = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.75, 2, 2.5, 3, 4, 5, 6, 7, 8, 9,
                 10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40, 45, 50, 75, 100,
                 101, 101, 101, 101]


def _level(xp):
    level = 0
    for mult in PRESTIGE_MULT:
        for req in EXP_PHASED:
            for _ in range(10):
                if xp < req * mult:
                    return level
                xp -= req * mult
                level += 1
    return level


def run(cmd, p, rank, stats, args, footer):
    pit = stats.get('Pit') or {}
    profile = pit.get('profile') or {}
    ptl = pit.get('pit_stats_ptl') or {}
    level = _level(profile.get('xp') or 0)
    return build_string(cmd.msg('pit.layout'), [
        rank + (p.get('displayname') or ''),
        level % 120,
        len(profile.get('prestiges') or []),
        number_format(ptl.get('max_streak')),
        number_format(ptl.get('kills')),
        number_format(ptl.get('assists')),
        number_format(ptl.get('deaths')),
        div(ptl.get('kills'), ptl.get('deaths')),
        div((ptl.get('kills') or 0) + (ptl.get('assists') or 0), ptl.get('deaths')),
    ])
