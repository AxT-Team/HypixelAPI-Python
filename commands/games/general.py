# -*- coding: utf-8 -*-
"""全局信息 (/hyp <玩家>)"""
import math
import time

from ...utils import build_string, format_time, json_get, number_format


def run(cmd, p, rank, stats, args, footer):
    online = bool(p.get('lastLogout')) and (p.get('lastLogout') or 0) < (p.get('lastLogin') or 0)
    session = None
    if online:
        result, _ = cmd.api.status(p.get('uuid'))
        if result and result.get('success'):
            session = result.get('session')

    ach = p.get('achievements') or {}
    network_exp = p.get('networkExp') or 0
    level = 1 if network_exp < 0 else math.sqrt(12.25 + 0.0008 * network_exp) - 2.5

    if online:
        secs = time.time() - (p.get('lastLogin') or 0) / 1000
        online_text = build_string(cmd.msg('general.placeholders.online'),
                                   [format_time(secs, True, 'H:i:s')])
        status_text = build_string(cmd.msg('general.placeholders.status'), [
            ((cmd.msg('games.' + str(session.get('gameType'))) or (' ' + str(session.get('gameType')) + ' '))
             if session and session.get('gameType') else cmd.msg('general.placeholders.no_access')),
            (cmd.msg('modes.' + str(session.get('mode'))) or (' ' + str(session.get('mode')) + ' '))
            if session and session.get('mode') else '',
            (cmd.msg('maps.' + str(session.get('map'))) or (' ' + str(session.get('map')) + ' '))
            if session and session.get('map') else '',
        ])
    else:
        online_text = build_string(cmd.msg('general.placeholders.last_logout'), [
            cmd.msg('general.placeholders.no_access') if not p.get('lastLogout')
            else format_time(p.get('lastLogout'), offset=cmd.timezone_offset)
        ])
        status_text = ''

    return build_string(cmd.msg('general.layout'), [
        rank + (p.get('displayname') or ''),
        level,
        number_format(p.get('karma')),
        number_format(p.get('achievementPoints')),
        number_format(ach.get('general_wins')),
        number_format(ach.get('general_quest_master')),
        number_format(ach.get('general_challenger')),
        '',
        cmd.msg('general.placeholders.no_access_or_data') if not p.get('userLanguage')
        else (cmd.msg('languages.' + p['userLanguage']) or (' ' + p['userLanguage'] + ' ')),
        cmd.msg('general.placeholders.no_access_or_data') if not p.get('mostRecentGameType')
        else (cmd.msg('games.' + p['mostRecentGameType']) or (' ' + p['mostRecentGameType'] + ' ')),
        cmd.msg('general.placeholders.no_access') if not p.get('firstLogin')
        else format_time(p.get('firstLogin'), offset=cmd.timezone_offset),
        cmd.msg('general.placeholders.no_access') if not p.get('lastLogin')
        else format_time(p.get('lastLogin'), offset=cmd.timezone_offset),
        online_text,
        status_text,
        footer,
        number_format(json_get(p, 'giftingMeta.ranksGiven', 0)),
    ])
