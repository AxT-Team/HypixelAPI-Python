# -*- coding: utf-8 -*-
"""通用工具: PHP 风格格式化 / 时间格式化 / 带缓存的 HTTP 请求"""
import hashlib
import json
import os
import re
import time
import urllib.parse
import urllib.request

CACHE_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')

_FMT_RE = re.compile(
    r"%(?:(\d+)\$)?([-+ 0']*)(\d+)?(?:\.(\d+))?(l?)([bcdeEfFgGosuxX%])"
)


def _format_one(arg, flags, width, precision, conv):
    if conv == 's':
        s = '' if arg is None else str(arg)
        if precision is not None:
            s = s[:int(precision)]
        if width:
            w = int(width)
            if '-' in flags:
                s = s.ljust(w)
            elif '0' in flags:
                s = s.rjust(w, '0')
            else:
                s = s.rjust(w)
        return s
    if conv in 'duxX':
        try:
            n = int(round(float(arg or 0)))
        except (TypeError, ValueError):
            n = 0
        spec = ''
        if '-' in flags:
            spec += '<'
        if '+' in flags:
            spec += '+'
        if '0' in flags and '-' not in flags:
            spec += '0'
        if width:
            spec += width
        spec += {'d': 'd', 'u': 'd', 'x': 'x', 'X': 'X'}[conv]
        return format(n, spec)
    if conv in 'eEfFgG':
        try:
            n = float(arg or 0)
        except (TypeError, ValueError):
            n = 0.0
        spec = ''
        if '-' in flags:
            spec += '<'
        if '+' in flags:
            spec += '+'
        if '0' in flags and '-' not in flags:
            spec += '0'
        if width:
            spec += width
        spec += '.' + (precision if precision is not None else '6')
        spec += conv if conv in 'eEgG' else 'f'
        return format(n, spec)
    return '' if arg is None else str(arg)


def php_vsprintf(fmt, args):
    """模拟 PHP vsprintf, 支持 %1$s 位置参数与 %.3lf 等格式"""
    pos = [0]

    def repl(m):
        argnum, flags, width, precision, _l, conv = m.groups()
        if conv == '%':
            return '%'
        if argnum is not None:
            idx = int(argnum) - 1
        else:
            idx = pos[0]
            pos[0] += 1
        arg = args[idx] if 0 <= idx < len(args) else None
        return _format_one(arg, flags or '', width, precision, conv)

    return _FMT_RE.sub(repl, fmt)


def build_string(layout, placeholders=None):
    """按 PHP vsprintf 风格拼接多行文本"""
    placeholders = placeholders or []
    if isinstance(layout, list):
        joined = '\n'.join('' if x is None else str(x) for x in layout)
        return php_vsprintf(joined, placeholders).replace('\n\n', '\n')
    return php_vsprintf(str(layout), placeholders)


def number_format(num, decimals=0):
    """模拟 PHP number_format, None 按 0 处理"""
    try:
        n = float(num or 0)
    except (TypeError, ValueError):
        n = 0.0
    if decimals == 0:
        return format(int(round(n)), ',d')
    return format(round(n, decimals), ',.{}f'.format(decimals))


def div(a, b, nd=3):
    """安全除法, 任一为 0/None 时返回 0"""
    if not a or not b:
        return 0
    return round(a / b, nd)


_PHP_TO_STRFTIME = {
    'Y': '%Y', 'm': '%m', 'd': '%d',
    'H': '%H', 'i': '%M', 's': '%S',
}


def format_time(timestamp, in_seconds=False, fmt='Y-m-d H:i', offset=0):
    """gmdate 风格时间格式化, None 按 0 处理"""
    ts = timestamp or 0
    secs = round(ts) if in_seconds else round(ts / 1000) + offset
    strf = ''.join(_PHP_TO_STRFTIME.get(c, c) for c in fmt)
    return time.strftime(strf, time.gmtime(secs))


def get_url(url, query=None, cache_expiration=0, timeout=15):
    """带文件缓存的 GET 请求, 返回 (body, status) 失败时 body 为 None"""
    query = query or {}
    full_url = url + '?' + urllib.parse.urlencode(query)
    os.makedirs(CACHE_DIRECTORY, exist_ok=True)
    cache_file = os.path.join(CACHE_DIRECTORY, hashlib.md5(full_url.encode()).hexdigest())
    if os.path.isfile(cache_file) and time.time() - os.path.getmtime(cache_file) <= cache_expiration:
        with open(cache_file, 'r', encoding='utf-8') as f:
            return f.read(), 200

    headers = {'User-Agent': 'HypixelCheckPy/1.0'}
    # 根据最新 api.hypixel.net 文档, API Key 通过 API-Key 请求头传递
    if 'key' in query:
        q = dict(query)
        headers['API-Key'] = q.pop('key')
        full_url_req = url + '?' + urllib.parse.urlencode(q)
    else:
        full_url_req = full_url
    req = urllib.request.Request(full_url_req, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode('utf-8')
            status = resp.status
    except urllib.error.HTTPError as e:
        return None, e.code
    except Exception:
        return None, 0
    if status == 200:
        with open(cache_file, 'w', encoding='utf-8') as f:
            f.write(body)
        return body, 200
    return None, status


def json_get(data, path, default=None):
    """按 a.b.c 路径取 JSON 值"""
    cur = data
    for key in path.split('.'):
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        else:
            return default
    return cur


def size_format(byte):
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    pos = 0
    b = float(byte)
    while b >= 1024 and pos < len(units) - 1:
        b /= 1024
        pos += 1
    return '{} {}'.format(round(b, 2), units[pos])


def plain_string(formatted):
    """去除 Minecraft 颜色代码"""
    if formatted is None:
        return None
    return re.sub('§[0-9a-fk-or]', '', str(formatted))
