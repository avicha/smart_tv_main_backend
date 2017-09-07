# coding=utf-8
from __future__ import division
from flask import Blueprint
from backend_common.controllers.base import BaseController
from backend_common.middlewares.request_service import get_request_params
from backend_common.services.crawler.netease import search_songs as netease_search_songs
from backend_common.services.crawler.qq import search_songs as qq_search_songs
from backend_common.services.crawler.xiami import search_songs as xiami_search_songs

song_blueprint = Blueprint('song', __name__)


def get_text_similarity(word, text):
    if not word:
        return 1
    elif not text:
        return 0
    else:
        word_len = len(word)
        text_len = len(text)
        if word in text:
            return 0.8 + word_len/text_len * 0.2
        else:
            equals_num = 0
            for i in range(1, word_len):
                if word[i] in text:
                    equals_num = equals_num + 1
            return 0.8 * equals_num / word_len + equals_num / text_len * 0.2


class SongController(BaseController):

    @classmethod
    def remove_unavailable_songs(cls, songs):
        return filter(lambda x: x.get('status') != -1, songs)

    @classmethod
    def uniq_songs(cls, songs):
        song_hash = {}
        for song in songs:
            song_name = song.get('name')
            singer_name = song.get('singer_name')
            key = '_'.join([song_name, singer_name])
            song_hash.setdefault(key, song)
        return song_hash.values()

    @classmethod
    def sort_songs(cls, songs, **kwargs):
        songs.sort(key=lambda song: cls.weight_song(song, **kwargs), reverse=True)
        return songs

    @classmethod
    def weight_song(cls, song, **kwargs):
        keywords = kwargs.get('keywords')
        # 歌曲名权重
        song_name_value = get_text_similarity(keywords, song.get('name'))
        song_name_weight = 10000
        song_name_score = song_name_value * song_name_weight
        # 专辑名权重
        album_name_value = get_text_similarity(keywords, song.get('album').get('name'))
        album_name_weight = 8000
        album_name_score = album_name_value * album_name_weight
        # 歌手名权重
        singer_name_value = get_text_similarity(keywords, song.get('singer_name'))
        singer_name_weight = 5000
        singer_name_score = singer_name_value * singer_name_weight
        # 歌曲排序权重
        song_sequence_value = -song.get('sequence')
        song_sequence_weight = 1
        song_sequence_score = song_sequence_value * song_sequence_weight
        # 设置歌曲权重最高的是因为歌名、专辑名、歌手名还是歌词
        max_score = max(song_name_score, album_name_score, singer_name_score)
        extract = max(song_name_value, album_name_value, singer_name_value)
        if song_name_score or album_name_score or singer_name_score:
            recommend_type = [song_name_score, album_name_score, singer_name_score].index(max_score) + 1
        else:
            recommend_type = 4
        song.setdefault('extrace', extract)
        song.setdefault('recommend_type', recommend_type)
        # 合计歌曲的权重
        weight = max_score + song_sequence_score
        return weight

    @classmethod
    @get_request_params()
    def search(cls, data):
        search_songs = []
        total_rows = 0
        keywords = data.get('keywords')
        page = int(data.get('page', 1))
        limit = int(data.get('limit', 20))
        for search_fn in [netease_search_songs, qq_search_songs, xiami_search_songs]:
            songs, total = search_fn(keywords, page=page, limit=limit)
            search_songs.extend(songs)
            if total > total_rows:
                total_rows = total
        results = cls.remove_unavailable_songs(search_songs)
        results = cls.uniq_songs(results)
        results = cls.sort_songs(results, keywords=keywords)
        print results
        return cls.success_with_list_result(total_rows, results)
