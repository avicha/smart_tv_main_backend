# coding=utf-8
import requests
import json

API_URL = 'https://c.y.qq.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Referer': 'https://y.qq.com/portal/search.html'
}
actions = [
    'play_lq',  # 普通音质播放权限位 （0：不可以播放 1：可以播放）
    'play_hq',  # HQ音质播放权限位 （0：不可以播放 1：可以播放）
    'play_sq',  # SQ音质播放权限位 （0：不可以播放 1：可以播放）
    'down_lq',  # 普通音质下载权限位 （0：不可以下载 1：可以下载）
    'down_hq',  # HQ音质下载权限位 （0：不可以下载 1：可以下载）
    'down_sq',  # SQ音质下载权限位 （0：不可以下载 1：可以下载）
    'soso',     # 地球展示权限位  （0：库内不展示地球 1：展示地球标志）
    'fav',      # 收藏权限位  （0：无权限 1：有权限）
    'share',    # 分享权限位  （0：无权限 1：有权限）
    'bgm',      # 背景音乐权限位  （0：无权限 1：有权限）
    'ring',     # 铃声设置权限位  （0：无权限 1：有权限）
    'sing',     # 唱这首歌权限位  （0：无权限 1：有权限）
    'radio',    # 单曲电台权限位  （0：无权限 1：有权限）
    'try',      # 试听权限位 （0：不可以试听 1：可以试听）
    'give'  # 赠送权限位 （0：不可以赠送 1：可以赠送）
]


def search_songs(keywords, page, limit):
    payload = {
        'format': 'json',
        'w': keywords,
        'n': limit,
        'p': page,
        'new_json': 1,
        'aggr': 1,
        'cr': 1
    }
    r = requests.get('%s/soso/fcgi-bin/client_search_cp' % API_URL, params=payload, headers=headers)
    resp = r.json()
    if not resp.get('code'):
        result = resp.get('data').get('song')
        total_rows = result.get('totalnum')
        songs = []
        for i, obj in enumerate(result.get('list')):
            singer = obj.get('singer')
            album = obj.get('album')
            switch = obj.get('action').get('switch', 403)
            switchs = bin(switch)[2:-1][::-1]
            action = {}
            for i, x in enumerate(actions):
                action[x] = True if switchs[i:i+1] == '1' else False
            action['play'] = False
            if action['play_lq'] or action['play_hq'] or action['play_sq']:
                action['play'] = True
            payplay = obj.get('pay').get('pay_play')
            tryplay = False
            if action.get('try') and obj.get('file').get('size_try'):
                tryplay = True
            if payplay:
                status = 0
            elif tryplay:
                status = 2
            elif action.get('play'):
                status = 1
            else:
                status = -1
            song = {
                'sequence': i,
                'id': obj.get('mid'),
                'name': obj.get('name'),
                'alias': obj.get('subtitle'),
                'duration': obj.get('interval'),
                'singer_name': ','.join(map(lambda x: x.get('name'), singer)),
                'artists': map(lambda o: {'id': o.get('mid'), 'name': o.get('name'), 'alias': o.get('title')}, singer),
                'mv': obj.get('mv').get('vid') or None,
                'album': {
                    'id': album.get('mid'),
                    'name': album.get('name'),
                    'cover': 'https://y.gtimg.cn/music/photo_new/T002R300x300M000%s.jpg' % album.get('mid'),
                    'coverBig': 'https://y.gtimg.cn/music/photo_new/T002R500x500M000%s.jpg' % album.get('mid'),
                    'coverSmall': 'https://y.gtimg.cn/music/photo_new/T002R150x150M000%s.jpg' % album.get('mid'),
                },
                'source': 2,
                'status': status
            }
            songs.append(song)
        return songs, total_rows
    else:
        print(resp)
        return [], 0
