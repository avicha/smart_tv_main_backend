# coding=utf-8
import requests
import json
import re

API_URL = 'https://api.xiami.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Referer': 'https://h.xiami.com/index.html?f=&from='
}


def search_songs(keywords, page, limit):
    data = {
        'v': '2.0',
        'app_key': 1,
        'key': keywords,
        'page': page,
        'limit': limit,
        'callback': 'jsonp',
        'r': 'search/songs'
    }
    r = requests.get('%s/web' % API_URL, params=data, headers=headers)
    json_text = re.match(r'^jsonp\(([\s\S]+)\)$', r.text).group(1)
    resp = json.loads(json_text)
    if resp.get('state') == 0:
        total_rows = resp.get('data').get('total')
        songs = [{
            'sequence': i,
            'id': str(x.get('song_id')),
            'name': x.get('song_name'),
            'alias': '',
            'duration': 0,
            'singer_name': x.get('artist_name'),
            'artists': [{'id': str(x.get('artist_id')), 'name': x.get('artist_name'), 'alias': ''}],
            'mv': None,
            'album': {
                'id': str(x.get('album_id')),
                'name': x.get('album_name'),
                'cover': x.get('album_logo'),
                'coverBig': x.get('album_logo').replace('1.jpg', '4.jpg'),
                'coverSmall': x.get('album_logo').replace('1.jpg', '2.jpg'),
            },
            'source': 3,
            'status': 0 if x.get('need_pay_flag') else (2 if x.get('demo') else 1)
        } for i, x in enumerate(resp.get('data').get('songs'))]
        return songs, total_rows
    else:
        return [], 0
