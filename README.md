# HypixelCheck

一个模块化的 Hypixel 玩家数据查询 Python 包。传入一条查询命令字符串，返回排版好的中文统计信息文本，适合直接接入 QQ 机器人等聊天机器人。

原为 PHP 版 HypixelCheck (基于 SpelakoCore) 的完全重构版:

- **纯 Python 标准库**, 无任何第三方依赖, Python 3.7+
- **API 包形式**, 直接 import 调用, 无需再部署 HTTP 服务
- **对齐最新 [api.hypixel.net](https://api.hypixel.net) v2 文档**: API Key 通过 `API-Key` 请求头认证
- **全字段容错**: 玩家缺失的统计字段一律按 0 / 空处理, 不会因新地图新模式缺字段而报错
- **新游戏/新模式**: 羊毛游戏 (WoolGames)、决斗新模式、僵尸末日新地图 (外星游乐园、监狱) 等
- **内置文件缓存与用户冷却**, 减少 API 消耗

## 安装

无需安装依赖, 将 `HypixelAPI-Python/` 目录放入你的项目 (或作为 git submodule / 直接 clone):

```bash
git clone https://github.com/AxT-Team/HypixelAPI-Python.git
```

## 配置

编辑 `hypixelcheck/config.json`:

```jsonc
{
    "hypixel": {
        "resource": "hypixel.json",          // 本地化资源文件名 (resources/ 下)
        "api_key": "你的 Hypixel API Key",    // 在 https://developer.hypixel.net 申请
        "timezone_offset": 28800             // 时间显示时区偏移(秒), 28800 = UTC+8
    },
    "staffs": ["管理员用户ID"],               // 管理员不受冷却限制
    "cooldown": 10,                          // 每用户查询冷却(秒)
    "cooldown_message": "获取速度太快了啦!"    // 冷却期间的提示
}
```

## 快速开始

```python
from hypixelcheck import HypixelCheck

checker = HypixelCheck()  # 默认读取包内 config.json, 也可传入自定义路径

# 同步调用
text = checker.execute('/hyp Technoblade bw', user_id)
print(text)

# asyncio 环境 (aiohttp 机器人等)
text = await checker.execute_async('/hyp Technoblade bw', user_id)
```

`execute(text, user)`:

| 参数 | 说明 |
| --- | --- |
| `text` | 完整命令字符串, 如 `/hyp 玩家名 zb aa` |
| `user` | 调用者标识 (任意字符串), 用于冷却计算 |
| 返回值 | 排版好的结果字符串; 命令不匹配时返回 `None` |

## 命令一览

基本格式: `/hyp <玩家名> [分类] [参数...]` (`/hypixel` 亦可)

| 分类 | 别名 | 说明 |
| --- | --- | --- |
| (不填) | general | 全局信息: 等级、人品值、成就点、在线状态等 |
| g | guild | 公会信息 |
| bw | bedwars | 起床战争, 可加模式: `solo` `doubles` `3v3v3v3` `4v4v4v4` `4v4`, 以及 `doubles_rush` `4v4v4v4_ultimate` `doubles_lucky` 等变体 |
| sw | skywars | 空岛战争 |
| uhc | - | 极限生存冠军 |
| pit | thepit | 天坑乱斗 |
| mw | megawalls | 超级战墙 |
| bsg | blitzsg, hungergames | 闪电饥饿游戏 |
| duel | duels | 决斗游戏, 可加模式: `classic` `op` `uhc` `sumo` `bridge` `sw` `mw` `bow` `potion` `combo` `blitz` `bowspleef` 及 `_doubles` 等变体 |
| ww | woolgames, woolwars | 羊毛游戏 (羊毛战争/甜蜜战争/夺羊大战) |
| bb | buildbattle | 建筑大师 |
| mm | murdermystery | 密室杀手, 可加模式/地图序号, 如 `/hyp 玩家 mm 1` |
| zb | zombies | 僵尸末日, 可加地图: `de`(穷途末路) `bb`(坏血之宫) `aa`(外星游乐园) `pr`(监狱), 及难度: `normal`(普通) `hard`(困难) `rip`(安息) |
| sb | skyblock | 空岛生存: `sb` 列出存档, `sb sk [存档]` 查技能, `sb a [存档] [页数]` 查拍卖 |
| r | recent | 最近游玩记录, 可加页数 |
| p | parkour | 大厅跑酷记录, 可加大厅序号查看存档点详情 |

### 缓存管理

| 命令 | 说明 |
| --- | --- |
| `/hyp cache` / `/hyp cache stats` | 查看缓存文件数量与占用 |
| `/hyp cache clean` | 清空全部缓存文件 |

### 示例

```text
/hyp _jebbb              -> 全局信息
/hyp _jebbb bw doubles   -> 起床战争双人模式
/hyp _jebbb zb aa        -> 僵尸末日·外星游乐园
/hyp _jebbb duel bridge  -> 战桥决斗
/hyp _jebbb sb sk 1      -> SkyBlock 1号存档技能
/hyp _jebbb r 2          -> 最近游玩第2页
```

## 目录结构

```
hypixelcheck/
├── __init__.py          # 对外入口 (HypixelCheck, execute / execute_async)
├── core.py              # 命令注册 / 冷却 / 资源加载
├── api.py               # Hypixel API v2 客户端 (API-Key 请求头)
├── utils.py             # PHP 风格格式化 / 时间格式化 / 带缓存 HTTP 请求
├── config.json          # API Key, 时区, 冷却配置
├── resources/
│   └── hypixel.json     # 中文本地化: 布局模板 / 游戏、模式、地图译名
├── cache/               # 运行时自动创建的 HTTP 缓存目录
└── commands/
    ├── hypixel.py       # /hyp 调度器: 玩家查询、分类分发、缓存管理
    └── games/           # 各游戏模块, 每个游戏一个文件
        ├── general.py   ├── guild.py    ├── bedwars.py
        ├── skywars.py   ├── duels.py    ├── uhc.py
        ├── pit.py       ├── megawalls.py├── blitz.py
        ├── buildbattle.py ├── woolgames.py ├── murdermystery.py
        ├── zombies.py   ├── skyblock.py ├── recent.py
        └── parkour.py
```

## 扩展新游戏

每个游戏模块只需实现一个函数:

```python
# commands/games/mygame.py
def run(cmd, p, rank, stats, args, footer):
    """
    cmd    -- HypixelCommand 调度器 (cmd.api 调 API, cmd.msg(key) 取本地化文本)
    p      -- Hypixel API 返回的 player 对象 (dict)
    rank   -- 已格式化的 "[MVP+] " 等前缀
    stats  -- p['stats'] (dict, 保证非 None)
    args   -- 分词后的命令参数列表
    footer -- 页脚文本
    返回排版好的字符串
    """
    s = stats.get('MyGame') or {}
    ...
```

然后在 `commands/hypixel.py` 的 handlers 注册表中加一行:

```python
(mygame, ['mygame', 'mg']),
```

布局模板放在 `resources/hypixel.json`, 使用 PHP vsprintf 风格占位符 (`%1$s`, `%2$d`, `%3$.3f`), 由 `utils.build_string()` 渲染, 模板为字符串数组时按行拼接。

## 机器人接入示例 (axtbot)

```python
_checker = None

async def get_hypixel_info(command, userid):
    global _checker
    if _checker is None:
        from hypixelcheck import HypixelCheck
        _checker = HypixelCheck()
    result = await _checker.execute_async(command, userid)
    return result if result is not None else "未知的命令。"
```

## 缓存机制

- 每个 API 请求按 URL 哈希缓存到 `cache/` 目录, 玩家数据默认 300 秒、在线状态 10 秒、最近游玩 45 秒
- 命中缓存时不发起网络请求; 过期自动重新拉取
- Hypixel 限流 (HTTP 429) 时返回友好提示而非报错

## 致谢与许可

- 消息布局与本地化文本源自 [Spelako Project](https://github.com/Spelako) 的 SpelakoCore (AGPL-3.0), 本项目为其查询功能的 Python 重构
- 数据来源: [Hypixel Public API](https://api.hypixel.net), 使用请遵守其 [服务条款](https://developer.hypixel.net/policies)

本项目建议以 AGPL-3.0 许可发布 (沿用上游许可要求)。
