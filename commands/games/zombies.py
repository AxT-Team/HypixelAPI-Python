# -*- coding: utf-8 -*-
"""僵尸末日 (/hyp <玩家> zb [地图] [难度]), 所有字段均容错缺失"""
from ...utils import build_string, div, format_time, number_format

_AA_BOSSES = ['giant', 'the_old_one', 'giant_rainbow', 'world_ender']
MAPS = {
    'deadend': (('_deadend', 'Dead End'), ['tnt', 'inferno', 'broodmother']),
    'de': (('_deadend', 'Dead End'), ['tnt', 'inferno', 'broodmother']),
    'badblood': (('_badblood', 'Bad Blood'), ['king_slime', 'wither', 'herobrine']),
    'bb': (('_badblood', 'Bad Blood'), ['king_slime', 'wither', 'herobrine']),
    'alienarcadium': (('_alienarcadium', 'Alien Arcadium'), _AA_BOSSES),
    'aa': (('_alienarcadium', 'Alien Arcadium'), _AA_BOSSES),
    'prison': (('_prison', 'Prison'), ['prisoner_zombie_angry', 'corrupted_pigman', 'the_warden']),
    'pr': (('_prison', 'Prison'), ['prisoner_zombie_angry', 'corrupted_pigman', 'the_warden']),
    'all': (('', 'all'), None),
    'fastView': (('', 'fastView'), None),
}
DIFFICULTIES = {
    'normal': ('_normal', 'normal'), 'norm': ('_normal', 'normal'),
    'hard': ('_hard', 'hard'), 'rip': ('_rip', 'rip'),
    'general': ('', 'general'),
}


def run(cmd, p, rank, stats, args, footer):
    ar = stats.get('Arcade') or {}
    a3 = args[3] if len(args) > 3 else 'fastView'
    if a3 not in MAPS:
        return build_string(cmd.msg('zb.info.unknown_map'))
    map_keys, boss_keys = MAPS[a3]

    def g(key):
        return ar.get(key) or 0

    if map_keys[1] == 'fastView':
        def cell(mapdiff):
            wins = g('wins_zombies' + mapdiff)
            if wins > 0:
                return number_format(wins)
            if g('total_rounds_survived_zombies' + mapdiff) == 0:
                return '-'
            return '[' + number_format(g('best_round_zombies' + mapdiff)) + ']'
        return build_string(cmd.msg('zb.layout_fastView'), [
            rank + (p.get('displayname') or ''),
            number_format(g('total_rounds_survived_zombies')),
            number_format(g('wins_zombies')),
            100 * div(g('bullets_hit_zombies'), g('bullets_shot_zombies')),
            100 * div(g('headshots_zombies'), g('bullets_hit_zombies')),
            cell('_deadend_normal'), cell('_deadend_hard'), cell('_deadend_rip'),
            cell('_badblood_normal'), cell('_badblood_hard'), cell('_badblood_rip'),
            cell('_alienarcadium_normal'),
            cell('_prison_normal'), cell('_prison_hard'), cell('_prison_rip'),
            footer,
        ])

    if map_keys[0] == '_alienarcadium':
        # 外星游乐园只有普通难度
        diff_arg = 'normal'
    else:
        diff_arg = args[4] if len(args) > 4 else 'general'
    if diff_arg not in DIFFICULTIES:
        return build_string(cmd.msg('zb.info.unknown_difficulty'))
    diff = DIFFICULTIES[diff_arg]
    suffix = map_keys[0] + diff[0]

    records = '' if diff[1] == 'general' else build_string(
        cmd.msg('zb.placeholders.records'), [
            format_time(g('fastest_time_10_zombies' + suffix), True, 'H:i:s'),
            format_time(g('fastest_time_20_zombies' + suffix), True, 'H:i:s'),
            format_time(g('fastest_time_30_zombies' + suffix), True, 'H:i:s'),
        ])

    if map_keys[1] == 'all':
        extra = build_string(cmd.msg('zb.placeholders.shots'), [
            number_format(g('bullets_shot_zombies')),
            number_format(g('bullets_hit_zombies')),
            number_format(g('headshots_zombies')),
            100 * div(g('bullets_hit_zombies'), g('bullets_shot_zombies')),
            100 * div(g('headshots_zombies'), g('bullets_hit_zombies')),
        ])
    else:
        is_aa = map_keys[0] == '_alienarcadium'
        placeholders = [
            cmd.msg('zb.placeholders.bosses.' + boss_keys[0]),
            number_format(g(boss_keys[0] + '_zombie_kills_zombies')),
            cmd.msg('zb.placeholders.bosses.' + boss_keys[1]),
            number_format(g(boss_keys[1] + '_zombie_kills_zombies')),
            cmd.msg('zb.placeholders.bosses.' + boss_keys[2]),
            number_format(g(boss_keys[2] + '_zombie_kills_zombies')),
        ]
        if is_aa:
            placeholders += [
                cmd.msg('zb.placeholders.bosses.' + boss_keys[3]),
                number_format(g(boss_keys[3] + '_zombie_kills_zombies')),
            ]
        extra = build_string(
            cmd.msg('zb.placeholders.boss_kills_aa' if is_aa else 'zb.placeholders.boss_kills'),
            placeholders)

    return build_string(cmd.msg('zb.layout'), [
        rank + (p.get('displayname') or ''),
        cmd.msg('maps.' + map_keys[1]),
        cmd.msg('zb.placeholders.difficulties.' + diff[1]),
        number_format(g('total_rounds_survived_zombies' + suffix)),
        number_format(g('wins_zombies' + suffix)),
        number_format(g('best_round_zombies' + suffix)),
        number_format(g('zombie_kills_zombies' + suffix)),
        number_format(g('players_revived_zombies' + suffix)),
        number_format(g('doors_opened_zombies' + suffix)),
        number_format(g('windows_repaired_zombies' + suffix)),
        number_format(g('times_knocked_down_zombies' + suffix)),
        number_format(g('deaths_zombies' + suffix)),
        records,
        extra,
        footer,
    ])
