# -*- coding: utf-8 -*-
"""密室杀手 (/hyp <玩家> mm [模式序号/地图序号/模式+地图序号])"""
from ...utils import build_string, div, format_time, number_format

MODES = {
    1: ('_MURDER_CLASSIC', 'MURDER_CLASSIC'),
    2: ('_MURDER_DOUBLE_UP', 'MURDER_DOUBLE_UP'),
    3: ('_MURDER_ASSASSINS', 'MURDER_ASSASSINS'),
    4: ('_MURDER_INFECTION', 'MURDER_INFECTION'),
    None: ('', 'all'),
}

MAPS = [
    ('_ancient_tomb', 'Ancient Tomb'), ('_aquarium', 'Aquarium'),
    ('_archives', 'Archives'), ('_archives_top_floor', 'Archives Top Floor'),
    ('_cruise_ship', 'Cruise Ship'), ('_darkfall', 'Darkfall'),
    ('_gold_rush', 'Gold Rush'), ('_headquarters', 'Headquarters'),
    ('_hollywood', 'Hollywood'), ('_hypixel_world', 'Hypixel World'),
    ('_library', 'Library'), ('_mountain', 'Mountain'),
    ('_san_peratico_v2', 'San Peratico v3'), ('_skyway_pier', 'Skyway Pier'),
    ('_snowfall', 'Snowfall'), ('_snowglobe', 'Snowglobe'),
    ('_subway', 'Subway'), ('_towerfall', 'Towerfall'),
    ('_transport', 'Transport'), ('_vilia', 'Vilia'),
    ("_widow's_den", "Widow's den"),
]


def run(cmd, p, rank, stats, args, footer):
    s = stats.get('MurderMystery') or {}
    a3 = args[3] if len(args) > 3 else None

    mode_code = None
    map_code = None
    if a3 is None:
        pass
    elif len(a3) == 1 and a3.isdigit() and 1 <= int(a3) <= 4:
        mode_code = int(a3)
    elif len(a3) == 1 and 'a' <= a3 <= 'u':
        map_code = ord(a3)
    elif (len(a3) == 2 and a3[0].isdigit() and 1 <= int(a3[0]) <= 4
          and 'a' <= a3[1] <= 'u'):
        mode_code = int(a3[0])
        map_code = ord(a3[1])
    else:
        return build_string(cmd.msg('mm.info.usage'), [p.get('displayname'), footer])

    mode = MODES[mode_code]
    mmap = MAPS[map_code - 97] if map_code is not None else ('', 'all')
    key = mmap[0] + mode[0]

    def v(name):
        return s.get(name + key)

    survived_ms = (v('total_time_survived_seconds') or 0) * 1000
    layout = [
        '%1$s 的密室杀手%25$s地图%2$s统计信息:',
        '硬币: %3$s | 当前 %4$s%% 杀手, %5$s%% 侦探' if mode[0] == '' else '',
        '胜场: %6$s | 胜率: %7$.3f%% | 金锭收集: %8$s',
        '侦探胜场: %12$s | 杀手胜场: %13$s' if mode[0] not in ('_MURDER_ASSASSINS', '_MURDER_INFECTION') else '',
        '死亡: %16$s',
        '击杀: %15$s | 陷阱击杀: %20$s ' if mode[0] != '_MURDER_INFECTION' else '',
        '近战击杀: %17$s | 飞刀击杀: %18$s | 弓箭击杀: %19$s' if mode[0] != '_MURDER_INFECTION' else '',
        '作为杀手击杀: %14$s | 英雄: %21$s' if mode[0] not in ('_MURDER_ASSASSINS', '_MURDER_INFECTION') else '',
        '侦探最快胜利: %22$ss | 杀手最快胜利: %23$ss' if mode[0] not in ('_MURDER_ASSASSINS', '_MURDER_INFECTION') else '',
        '作为感染者击杀: %26$s | 作为幸存者击杀: %27$s' if mode[0] in ('', '_MURDER_INFECTION') else '',
        '幸存者总存活: %9$s | 幸存者最久存活: %10$ss' if mode[0] in ('', '_MURDER_INFECTION') else '',
    ]
    return build_string(layout, [
        rank + (p.get('displayname') or ''),
        cmd.msg('modes.' + mode[1]),
        number_format(s.get('coins')),
        number_format(s.get('murderer_chance')),
        number_format(s.get('detective_chance')),
        number_format(v('wins')),
        div((v('wins') or 0) * 100, v('games')),
        number_format(v('coins_pickedup')),
        format_time(survived_ms, False, 'i:s') if survived_ms else '00:00',
        number_format(v('longest_time_as_survivor_seconds')),
        None,
        number_format(v('detective_wins')),
        number_format(v('murderer_wins')),
        number_format(v('kills_as_murderer')),
        number_format(v('kills')),
        number_format(v('deaths')),
        number_format(v('knife_kills')),
        number_format(v('thrown_knife_kills')),
        number_format(v('bow_kills')),
        number_format(v('trap_kills')),
        number_format(v('was_hero')),
        number_format(v('quickest_detective_win_time_seconds')),
        number_format(v('quickest_murderer_win_time_seconds')),
        footer,
        cmd.msg('maps.' + mmap[1]),
        number_format(v('kills_as_infected')),
        number_format(v('kills_as_survivor')),
    ])
