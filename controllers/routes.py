# coding=utf-8
from controllers.singer import singer_blueprint, SingerController
from controllers.album import album_blueprint, AlbumController
from controllers.song import song_blueprint, SongController
from controllers.tv import tv_blueprint, TVController


def init_app(current_app):
    singer_blueprint.add_url_rule('/search', 'search_api', SingerController.search, methods=['get', 'post'])
    current_app.register_blueprint(singer_blueprint, url_prefix='/api/singer')
    album_blueprint.add_url_rule('/search', 'search_api', AlbumController.search, methods=['get', 'post'])
    current_app.register_blueprint(album_blueprint, url_prefix='/api/album')
    song_blueprint.add_url_rule('/search', 'search_api', SongController.search, methods=['get', 'post'])
    current_app.register_blueprint(song_blueprint, url_prefix='/api/song')
    tv_blueprint.add_url_rule('/search', 'search_api', TVController.search, methods=['get', 'post'])
    current_app.register_blueprint(tv_blueprint, url_prefix='/api/tv')
