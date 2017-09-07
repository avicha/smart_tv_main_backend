# coding=utf-8
import requests
import json
import math

API_URL = 'http://music.163.com/weapi'
pubKey = '010001'
modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
nonce = '0CoJUm6Qyw8W8jud'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Origin': 'http://music.163.com',
    'Referer': 'http://music.163.com/search/'
}


def createSecretKey(size):
    import os
    return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]


def aesEncrypt(text, secKey):
    from Crypto.Cipher import AES
    import base64
    iv = '0102030405060708'
    cipher = AES.new(secKey, AES.MODE_CBC, iv)
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    return base64.b64encode(cipher.encrypt(text))


def rsaEncrypt(text, exponent, modulus):
    radix = 16
    text = text[::-1]
    rs = pow(int(text.encode('hex'), radix), int(exponent, radix), int(modulus, radix))
    return format(rs, 'x').zfill(256)


def asrsea(text, pubKey, modulus, nonce):
    res = {}
    secKey = createSecretKey(16)
    encText = aesEncrypt(text, nonce)
    res['params'] = aesEncrypt(encText, secKey)
    res['encSecKey'] = rsaEncrypt(secKey, pubKey, modulus)
    return res


def search_songs(keywords, page, limit):
    payload = {
        's': keywords,
        'type': 1,
        'limit': limit,
        'offset': (page - 1) * limit
    }
    data = asrsea(json.dumps(payload), pubKey, modulus, nonce)
    r = requests.post('%s/cloudsearch/get/web?csrf_token=' % API_URL, data=data, headers=headers)
    resp = r.json()
    if resp.get('code') == 200:
        result = resp.get('result')
        total_rows = result.get('songCount')
        songs = []
        for i, x in enumerate(result.get('songs')):
            album = x.get('al')
            singer = x.get('ar')
            mv = x.get('mv')
            song = {
                'sequence': i,
                'id': str(x.get('id')),
                'name': x.get('name'),
                'alias': ','.join(x.get('alia')),
                'duration': math.ceil(x.get('dt')/1000),
                'singer_name': ','.join(map(lambda x: x.get('name'), singer)),
                'artists': map(lambda o: {'id': str(o.get('id')), 'name': o.get('name'), 'alias': ','.join(o.get('alias'))}, singer),
                'mv': str(mv) if mv else None,
                'album': {
                    'id': str(album.get('id')),
                    'name': album.get('name'),
                    'cover': album.get('picUrl').replace('http://', 'https://') + '?param=250y250',
                    'coverBig': album.get('picUrl').replace('http://', 'https://') + '?param=param=400y400',
                    'coverSmall': album.get('picUrl').replace('http://', 'https://') + '?param=param=140y140',
                },
                'source': 1,
                'status': 0 if x.get('fee') else (1 if x.get('privilege').get('cp') else -1)
            }
            songs.append(song)
        return songs, total_rows
    else:
        print(resp)
        return [], 0
