# -*- coding: utf-8 -*-
"""建筑大师 (/hyp <玩家> bb)"""
from ...utils import build_string, number_format

LEVEL_TABLE = [100, 150, 250, 500, 1000, 1500, 1500, 2500, 2500, 5000, 5000]
RANK_NAMES = ['初来乍到', '未经雕琢', '初窥门径', '学有所成', '驾轻就熟', '历练老成',
              '技艺精湛', '炉火纯青', '技惊四座', '巧夺天工', '闻名于世', '名垂青史']


def run(cmd, p, rank, stats, args, footer):
    s = stats.get('BuildBattle') or {}
    score = s.get('score') or 0
    remaining = score
    i = 0
    while i < len(LEVEL_TABLE) and remaining >= LEVEL_TABLE[i]:
        remaining -= LEVEL_TABLE[i]
        i += 1
    chat_rank = RANK_NAMES[min(i, len(RANK_NAMES) - 1)]
    return build_string(cmd.msg('bb.layout'), [
        rank + (p.get('displayname') or ''),
        chat_rank,
        number_format(score),
        number_format(s.get('coins')),
        number_format(s.get('games_played')),
        number_format(s.get('wins')),
        number_format(s.get('total_votes')),
        number_format(s.get('super_votes')),
        number_format(s.get('wins_solo_normal')),
        number_format(s.get('wins_teams_normal')),
        number_format(s.get('wins_solo_pro')),
        number_format(s.get('wins_guess_the_build')),
        number_format(s.get('correct_guesses')),
    ])
