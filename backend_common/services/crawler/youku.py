# coding=utf-8
import requests
import time
from backend_common.models.mongodb import db
import backend_common.const.video_source as video_source
from backend_common.exceptions.base_error import BaseError


def get_cna():
    r = requests.get('http://log.mmstat.com/eg.js')
    if r.status_code is 200:
        return r.cookies.get('cna') or r.headers.get('ETag')
    else:
        return None


def get_ups(video_id, cna):
    print('cna: %s' % cna)
    payload = {
        'vid': video_id,
        'ccode': '0501',
        'client_ip': '0.0.0.0',
        'client_ts': time.time(),
        'utid': cna
    }
    headers = {
        'referer': 'http://m.youku.com/video/id_%s.html' % video_id
    }
    r = requests.get('https://ups.youku.com/ups/get.json', params=payload, headers=headers)
    resp = r.json()
    data = resp.get('data')
    if data.get('error'):
        error = data.get('error')
        raise BaseError(error.get('code'), error.get('note'))
    else:
        return data


def get_play_info(video_id):
    query = {'video_id': video_id, 'source': video_source.YOUKU}
    doc = db.video_play_infos.find_one(query, {'_id': 0})
    if doc:
        return doc.get('play_info')
    else:
        cna = get_cna()
        play_info = {}
        ups = get_ups(video_id, cna)
        play_info['video_types'] = filter(lambda x: x.get('type') in ['mp4sd', 'mp4hd', 'mp4hd2'], map(lambda x: {'width': x.get('width'), 'height': x.get('height'), 'url': x.get('m3u8_url'), 'type': x.get('stream_type'), 'lang': x.get('audio_lang'), 'duration': x.get('milliseconds_video')}, ups.get('stream')))
        next_part = ups.get('videos').get('next')
        previous_part = ups.get('videos').get('previous')
        play_info['next'] = {'video_id': next_part.get('encodevid'), 'source': video_source.YOUKU} if next_part else None
        play_info['previous'] = {'video_id': previous_part.get('encodevid'), 'source': video_source.YOUKU} if previous_part else None
        db.video_play_infos.update_one(query, {'$set': {'play_info': play_info}}, upsert=True)
        return play_info
