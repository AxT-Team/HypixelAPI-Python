# -*- coding: utf-8 -*-
"""起床战争 (/hyp <玩家> bw [模式])"""
from ...utils import build_string, div, json_get, number_format


def run(cmd, p, rank, stats, args, footer):
    s = stats.get('Bedwars') or {}
    mode_arg = args[3] if len(args) > 3 else None
    if not mode_arg:
        prefix = ''
        mode_name = cmd.msg('modes.all')
    else:
        mode_name = cmd.msg('modes.BEDWARS_' + mode_arg.upper())
        if not mode_name:
            replaced = mode_arg
            for old, new in [('solo', 'eight_one'), ('doubles', 'eight_two'),
                             ('3v3v3v3', 'four_three'), ('4v4v4v4', 'four_four'),
                             ('4v4', 'two_four')]:
                replaced = replaced.replace(old, new)
            mode_name = cmd.msg('modes.BEDWARS_' + replaced.upper())
            mode_arg = replaced
        if not mode_name:
            return build_string(cmd.msg('bw.info.usage'), [p.get('displayname')])
        prefix = mode_arg + '_'

    def v(key):
        return s.get(prefix + key)

    winstreak = v('winstreak')
    if winstreak is None and (v('wins_bedwars') or 0) != 0:
        ws_text = cmd.msg('bw.placeholders.win_strikes_no_access')
    else:
        ws_text = number_format(winstreak)

    return build_string(cmd.msg('bw.layout'), [
        rank + (p.get('displayname') or ''),
        mode_name,
        '' if mode_arg else build_string(cmd.msg('bw.placeholders.general_stats'), [
            number_format(json_get(p, 'achievements.bedwars_level', 0)),
            number_format(s.get('coins')),
        ]),
        number_format(v('beds_broken_bedwars')),
        number_format(v('beds_lost_bedwars')),
        ws_text,
        number_format(v('wins_bedwars')),
        number_format(v('losses_bedwars')),
        div(v('wins_bedwars'), v('losses_bedwars')),
        number_format(v('kills_bedwars')),
        number_format(v('deaths_bedwars')),
        div(v('kills_bedwars'), v('deaths_bedwars')),
        number_format(v('final_kills_bedwars')),
        number_format(v('final_deaths_bedwars')),
        div(v('final_kills_bedwars'), v('final_deaths_bedwars')),
        number_format(v('iron_resources_collected_bedwars')),
        number_format(v('gold_resources_collected_bedwars')),
        number_format(v('diamond_resources_collected_bedwars')),
        number_format(v('emerald_resources_collected_bedwars')),
        footer,
    ])
