# -*- coding: utf-8 -*-
"""最近游玩 (/hyp <玩家> r [页数])"""
import math

from ...utils import build_string, format_time


def run(cmd, p, rank, stats, args, footer):
    result, status = cmd.api.recent_games(p.get('uuid'))
    if result is None:
        return cmd.msg('info.request_failed' if status == 0 else 'info.incomplete_json')
    if not result.get('success'):
        return cmd.msg('info.incomplete_json')
    games = result.get('games')
    if not games:
        return build_string(cmd.msg('recent.info.no_data_or_access'), [p.get('displayname')])

    tot_pages = int(math.ceil(len(games) / 5))
    try:
        cur_page = int(args[3]) if len(args) > 3 else 1
    except ValueError:
        cur_page = 1
    cur_page = max(1, min(cur_page, tot_pages))
    entries = []
    for game in games[(cur_page - 1) * 5:cur_page * 5]:
        ended = game.get('ended')
        entries.append(build_string(
            cmd.msg('recent.placeholders.ended_game' if ended else 'recent.placeholders.ongoing_game'),
            [
                cmd.msg('games.' + str(game.get('gameType'))) or (' ' + str(game.get('gameType')) + ' '),
                cmd.msg('modes.' + str(game.get('mode'))) or (' ' + str(game.get('mode')) + ' '),
                cmd.msg('maps.' + str(game.get('map'))) or (' ' + str(game.get('map')) + ' '),
                format_time(game.get('date'), offset=cmd.timezone_offset),
                format_time(ended, offset=cmd.timezone_offset) if ended else '',
            ]))
    return build_string(cmd.msg('recent.layout'), [
        rank + (p.get('displayname') or ''),
        '\n'.join(entries),
        '' if tot_pages == 1 else build_string(
            cmd.msg('recent.placeholders.page_indicator'),
            [cur_page, tot_pages, p.get('displayname')]),
    ])
