# -*- coding: utf-8 -*-
"""决斗游戏 (/hyp <玩家> duel [模式])"""
from ...utils import build_string, div, number_format


def run(cmd, p, rank, stats, args, footer):
    s = stats.get('Duels') or {}
    mode_arg = args[3] if len(args) > 3 else None
    if not mode_arg:
        prefix = suffix = ''
        mode_name = cmd.msg('modes.all')
    else:
        mode_name = cmd.msg('modes.DUELS_' + mode_arg.upper())
        if not mode_name:
            mode_arg = mode_arg + '_duel'
            mode_name = cmd.msg('modes.DUELS_' + mode_arg.upper())
        if not mode_name:
            return build_string(cmd.msg('duels.info.usage'), [p.get('displayname')])
        prefix = mode_arg + '_'
        suffix = '_' + mode_arg

    def v(key):
        return s.get(prefix + key)

    kills_key = 'bridge_kills' if 'bridge' in prefix else 'kills'
    deaths_key = 'bridge_deaths' if 'bridge' in prefix else 'deaths'

    if s.get('best_overall_winstreak') is None and (v('wins') or 0) != 0:
        ws_text = cmd.msg('duels.placeholders.win_strikes_no_access')
    else:
        ws_text = build_string(cmd.msg('duels.placeholders.win_strikes'), [
            number_format(s.get('current_winstreak_mode' + suffix) if mode_arg
                          else s.get('current_winstreak')),
            number_format(s.get('best_winstreak_mode' + suffix) if mode_arg
                          else s.get('best_overall_winstreak')),
        ])

    return build_string(cmd.msg('duels.layout'), [
        rank + (p.get('displayname') or ''),
        mode_name,
        '' if mode_arg else build_string(cmd.msg('duels.placeholders.general_stats'), [
            number_format(s.get('coins')),
        ]),
        number_format(v('rounds_played')),
        number_format(v('wins')),
        number_format(v('losses')),
        div(v('wins'), v('losses')),
        ws_text,
        number_format(v(kills_key)),
        number_format(v(deaths_key)),
        div(v(kills_key), v(deaths_key)),
        '' if any(x in prefix for x in ('sumo', 'classic', 'potion')) else build_string(
            cmd.msg('duels.placeholders.bow_stats'), [
                number_format(v('bow_shots')),
                number_format(v('bow_hits')),
                100 * div(v('bow_hits'), v('bow_shots')),
            ]),
        number_format(v('melee_swings')),
        number_format(v('melee_hits')),
        100 * div(v('melee_hits'), v('melee_swings')),
        build_string(cmd.msg('duels.placeholders.gapples_eaten'), [
            number_format(v('golden_apples_eaten'))
        ]) if mode_arg and ('uhc' in prefix or 'combo' in prefix) else '',
        number_format(v('health_regenerated')),
        number_format(v('damage_dealt')),
        footer,
    ])
