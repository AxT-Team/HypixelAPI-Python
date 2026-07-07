# -*- coding: utf-8 -*-
"""大厅跑酷 (/hyp <玩家> p [大厅序号])"""
from ...utils import build_string, format_time

# (代码, 中文名, 存档点数量)
LOBBIES = [
    ('mainLobby2017', '主大厅', 3),
    ('Bedwars', '起床战争', 4),
    ('SkywarsAug2017', '空岛战争', 4),
    ('ArcadeGames', '街机游戏', 7),
    ('MurderMystery', '密室杀手', 4),
    ('TNT', '掘战游戏', 4),
    ('uhc', '极限生存冠军', 4),
    ('Prototype', '游戏实验室', 3),
    ('BuildBattle', '建筑大师', 4),
    ('Housing', '家园世界', 8),
    ('MegaWalls', '超级战墙', 4),
    ('BlitzLobby', '闪电饥饿游戏', 1),
    ('Warlords', '战争领主', 3),
    ('SuperSmash', '星碎英雄', 4),
    ('CopsnCrims', '警匪大战', 5),
    ('Duels', '决斗游戏', 4),
    ('Legacy', '经典游戏', 3),
    ('Tourney', '竞赛殿堂', 3),
    ('mainLobby2022', '主大厅2022', 5),
    ('SkywarsStandard2022', '空岛战争2022', 8),
    ('WoolGames', '羊毛游戏', 5),
    ('BedwarsSpring2023', '起床战争2023春季', 6),
    ('tntLobby2024', '掘战游戏2024', 5),
    ('CopsnCrims2024', '警匪大战2024', 8),
]


def _fmt_ms(t):
    return format_time(t, False, 'i:s') + '.' + '{:03d}'.format(int(t) % 1000)


def run(cmd, p, rank, stats, args, footer):
    completions = p.get('parkourCompletions') or {}
    checkpoints = p.get('parkourCheckpointBests') or {}
    lobby_arg = args[3] if len(args) > 3 else None

    def best_time(code):
        recs = completions.get(code) or []
        return recs[0].get('timeTook') if recs else None

    if not lobby_arg:
        lines = []
        for i, (code, name, _cp) in enumerate(LOBBIES):
            t = best_time(code)
            if t is not None:
                text = _fmt_ms(t)
            else:
                cps = checkpoints.get(code) or {}
                partial = cps.get('0') is not None or cps.get(0) is not None
                text = '未' + ('完全' if partial else '') + '完成'
            lines.append('{}. {}: {}'.format(i + 1, name, text))
        return build_string([
            '===大厅跑酷记录===', '%1$s', '==================',
            '%2$s', '==================',
            '使用 /hyp %3$s p <序号> 来查看详细信息.',
        ], [rank + (p.get('displayname') or ''), '\n'.join(lines), p.get('displayname')])

    try:
        lobby = int(lobby_arg)
    except ValueError:
        lobby = -1
    if 1 <= lobby <= len(LOBBIES):
        code, name, cp_count = LOBBIES[lobby - 1]
        cps = checkpoints.get(code) or {}
        lines = []
        for i in range(cp_count):
            t = cps.get(str(i), cps.get(i))
            lines.append('{}. {}'.format(i + 1, _fmt_ms(t) if t is not None else '未完成'))
        t = best_time(code)
        recs = completions.get(code) or []
        created = ''
        if t is not None and recs:
            created = format_time((recs[0].get('timeTook') or 0) + (recs[0].get('timeStart') or 0),
                                  fmt='Y-m-d H:i:s', offset=cmd.timezone_offset)
        return build_string([
            '%1$s 的%2$s跑酷每个存档点最佳记录:',
            '%3$s',
            '完成跑酷用时: %4$s',
            '记录创建于: %5$s' if t is not None else None,
        ], [
            rank + (p.get('displayname') or ''), name, '\n'.join(lines),
            _fmt_ms(t) if t is not None else '未完成',
            created,
        ])

    lines = ['- {}. {}'.format(i + 1, name) for i, (_c, name, _cp) in enumerate(LOBBIES)]
    return build_string([
        '未知的序号.', '目前支持的序号可以为下列之一(序号 - 中文名):', '%1$s',
    ], ['\n'.join(lines)])
