# -*- coding: utf-8 -*-
"""公会信息 (/hyp <玩家> g)"""
from ...utils import build_string, format_time, json_get, plain_string

LEVEL_TABLE = [100000, 150000, 250000, 500000, 750000, 1000000, 1250000,
               1500000, 2000000, 2500000, 2500000, 2500000, 2500000,
               2500000, 3000000]


def run(cmd, p, rank, stats, args, footer):
    result, status = cmd.api.guild_by_player(p.get('uuid'))
    if result is None:
        return cmd.msg('info.request_failed' if status == 0 else 'info.incomplete_json')
    if not result.get('success'):
        return cmd.msg('info.incomplete_json')
    g = result.get('guild')
    if not g:
        return build_string(cmd.msg('guild.info.guild_not_found'), [p.get('displayname')])

    exp = g.get('exp') or 0
    level = 0
    need = LEVEL_TABLE[0]
    while True:
        if level >= 15:
            break
        need = LEVEL_TABLE[level]
        exp -= need
        level += 1
        if exp < 0:
            break
    level += exp / need

    pref = cmd.msg('guild.placeholders.none')
    if g.get('preferredGames'):
        names = [(cmd.msg('games.' + game) or (' ' + game + ' '))
                 for game in g['preferredGames']]
        pref = ', '.join(names)

    return build_string(cmd.msg('guild.layout'), [
        rank + (p.get('displayname') or ''),
        g.get('name'),
        format_time(g.get('created'), offset=cmd.timezone_offset),
        level,
        plain_string(g.get('tag')) or '',
        len(g.get('members') or []),
        json_get(g, 'achievements.ONLINE_PLAYERS', 0),
        pref,
    ])
