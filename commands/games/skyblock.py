# -*- coding: utf-8 -*-
"""SkyBlock 空岛生存 (/hyp <玩家> sb [分类] [存档名/序号] [页数])"""
import math
import time

from ...utils import build_string, format_time, json_get, number_format

SKILLS = ['taming', 'farming', 'mining', 'combat', 'foraging',
          'fishing', 'enchanting', 'alchemy', 'carpentry', 'runecrafting']

LADDER = [0, 50, 175, 375, 675, 1175, 1925, 2925, 4425, 6425, 9925,
          14925, 22425, 32425, 47425, 67425, 97425, 147425, 222425,
          322425, 522425, 822425, 1222425, 1722425, 2322425, 3022425,
          3822425, 4722425, 5722425, 6822425, 8022425, 9322425,
          10722425, 12222425, 13822425, 15522425, 17322425, 19222425,
          21222425, 23322425, 25522425, 27822425, 30222425, 32722425,
          35322425, 38072425, 40972425, 44072425, 47472425, 51172425,
          55172425, 59472425, 64072425, 68972425, 74172425, 79672425,
          85472425, 91572425, 97972425, 104672425, 111672425]
RUNE_LADDER = [0, 50, 150, 275, 435, 635, 885, 1200, 1600, 2100, 2725,
               3510, 4510, 5760, 7325, 9325, 11825, 14950, 18950,
               23950, 30200, 38050, 47850, 60100, 75400, 94450]


def _skill_level(exp, runecrafting=False):
    ladder = RUNE_LADDER if runecrafting else LADDER
    level = 0
    for cur, required in enumerate(ladder):
        if exp > required:
            level = cur
    return level


def _profile_id(profiles, query):
    keys = list(profiles.keys())
    try:
        idx = int(query) - 1
        return keys[idx] if 0 <= idx < len(keys) else None
    except (TypeError, ValueError):
        pass
    for k, v in profiles.items():
        if str(v.get('cute_name', '')).lower() == str(query).lower():
            return v.get('profile_id') or k
    return None


def _profile_list_text(profiles):
    return '\n'.join('{}. {}'.format(i + 1, profiles[k].get('cute_name'))
                     for i, k in enumerate(profiles))


def _profile_not_found(p, profiles):
    return build_string([
        '无法找到玩家 %1$s 的此空岛生存存档.',
        '此玩家的 %2$d 个空岛生存存档 (序号 - 存档名):',
        '%3$s',
    ], [p.get('displayname'), len(profiles), _profile_list_text(profiles)])


def _skills(cmd, p, rank, profiles, args):
    query = args[4] if len(args) > 4 else 1
    profile_id = _profile_id(profiles, query)
    if not profile_id:
        return _profile_not_found(p, profiles)
    result, _ = cmd.api.skyblock_profile(profile_id)
    profile = result.get('profile') if result and result.get('success') else None
    member = json_get(profile or {}, 'members.' + (p.get('uuid') or ''), {}) or {}
    accessible = any(('experience_skill_' + sk) in member for sk in SKILLS)
    if accessible:
        levels = {sk: _skill_level(member.get('experience_skill_' + sk) or 0,
                                   sk == 'runecrafting')
                  for sk in SKILLS}
    else:
        ach = p.get('achievements') or {}
        levels = {
            'taming': ach.get('skyblock_domesticator') or 0,
            'farming': ach.get('skyblock_harvester') or 0,
            'mining': ach.get('skyblock_excavator') or 0,
            'combat': ach.get('skyblock_combat') or 0,
            'foraging': ach.get('skyblock_gatherer') or 0,
            'fishing': ach.get('skyblock_angler') or 0,
            'enchanting': ach.get('skyblock_augmentation') or 0,
            'alchemy': ach.get('skyblock_concoctor') or 0,
            'carpentry': 0, 'runecrafting': 0,
        }
    note = ('木工: %11$d | 符文合成: %12$d' if accessible else
            ('注意: 访问该玩家技能 API 时超时或失败, ' if profile is None
             else '注意: 该玩家技能信息被玩家在 API 设置中阻止, ') + '已显示为跨存档的最高等级.')
    return build_string([
        '%1$s 的空岛生存 %2$s 存档技能信息:' if accessible else '%1$s 的空岛生存技能信息:',
        '驯养: %3$d | 农业: %4$d',
        '挖矿: %5$d | 战斗: %6$d',
        '林业: %7$d | 钓鱼: %8$d',
        '附魔: %9$d | 酿造: %10$d',
        note,
    ], [
        rank + (p.get('displayname') or ''),
        json_get(profiles, profile_id + '.cute_name', ''),
        levels['taming'], levels['farming'], levels['mining'],
        levels['combat'], levels['foraging'], levels['fishing'],
        levels['enchanting'], levels['alchemy'],
        levels.get('carpentry', 0), levels.get('runecrafting', 0),
    ])


def _auctions(cmd, p, rank, profiles, args):
    query = args[4] if len(args) > 4 else 1
    profile_id = _profile_id(profiles, query)
    if not profile_id:
        return _profile_not_found(p, profiles)
    result, status = cmd.api.skyblock_auction(profile_id)
    if result is None:
        return cmd.msg('info.request_failed' if status == 0 else 'info.incomplete_json')
    if not result.get('success'):
        return cmd.msg('info.incomplete_json')
    cute = json_get(profiles, profile_id + '.cute_name', '')
    auctions = result.get('auctions')
    if not auctions:
        extra = ' 你可以尝试查询此玩家的其他存档.' if len(profiles) > 1 else ''
        return '找不到玩家 {} 的空岛生存 {} 存档中的物品拍卖信息.{}'.format(
            p.get('displayname'), cute, extra)
    auctions = list(reversed(auctions))
    tot_pages = int(math.ceil(len(auctions) / 5))
    try:
        cur_page = int(args[5]) if len(args) > 5 else 1
    except ValueError:
        cur_page = 1
    cur_page = max(1, min(cur_page, tot_pages))
    entries = []
    now = time.time()
    for item in auctions[(cur_page - 1) * 5:cur_page * 5]:
        end = item.get('end') or 0
        if item.get('bin'):
            entries.append(build_string([
                '# %1$s (%2$s)', '\t一口价: %3$s', '\t结束时间: %4$s', '\t状态: %5$s',
            ], [
                item.get('item_name'), item.get('tier'),
                number_format(item.get('starting_bid')),
                format_time(end, offset=cmd.timezone_offset),
                '已被购买' if item.get('claimed_bidders') else (
                    '进行中' if now < end / 1000 else '已结束, 无买主'),
            ]))
        else:
            entries.append(build_string([
                '# %1$s (%2$s)',
                '\t最高出价: %3$s' if now < end / 1000 else '\t成交价: %3$s',
                '\t出价数: %4$d', '\t起拍价: %5$s', '\t结束时间: %6$s', '\t状态: %7$s',
            ], [
                item.get('item_name'), item.get('tier'),
                number_format(item.get('highest_bid_amount')),
                len(item.get('bids') or []),
                number_format(item.get('starting_bid')),
                format_time(end, offset=cmd.timezone_offset),
                '进行中' if now < end / 1000 else '已结束',
            ]))
    return build_string([
        '%1$s 的空岛生存 %2$s 存档物品拍卖信息:',
        '%3$s',
        '当前展示 %4$d/%5$d 页.',
        '使用 /hyp %6$s sb a %7$s <页数> 来查看具体页数的拍卖信息.' if tot_pages > 1 else '',
    ], [
        rank + (p.get('displayname') or ''), cute, '\n'.join(entries),
        cur_page, tot_pages, p.get('displayname'), cute,
    ])


def run(cmd, p, rank, stats, args, footer):
    profiles = json_get(stats, 'SkyBlock.profiles') or {}
    sub = args[3] if len(args) > 3 else None

    if sub in ('skills', 'skill', 'sk', 's'):
        return _skills(cmd, p, rank, profiles, args)
    if sub in ('auctions', 'auction', 'au', 'a'):
        return _auctions(cmd, p, rank, profiles, args)
    if sub is None:
        return build_string([
            '%1$s 的 %2$d 个空岛生存存档 (序号 - 存档名):',
            '%3$s',
            '欲查询其空岛生存信息, 请使用此命令:',
            '/hyp %4$s sb <分类> [存档名/序号]',
            '目前支持的分类可以是下列之一:',
            '- skills, skill, sk, s',
            '- auctions, auction, au, a',
        ], [
            rank + (p.get('displayname') or ''), len(profiles),
            _profile_list_text(profiles), p.get('displayname'),
        ])
    return build_string([
        '未知的分类.',
        '目前支持的分类可以是下列之一:',
        '- skills, skill, sk, s',
        '- auctions, auction, au, a',
    ])
