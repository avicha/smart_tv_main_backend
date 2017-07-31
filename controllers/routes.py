# coding=utf-8
from controllers.singer import singer_blueprint, SingerController
from controllers.album import album_blueprint, AlbumController


def init_app(current_app):
    singer_blueprint.add_url_rule('/search', 'search_api', SingerController.search, methods=['get', 'post'])
    current_app.register_blueprint(singer_blueprint, url_prefix='/api/singer')
    album_blueprint.add_url_rule('/search', 'search_api', AlbumController.search, methods=['get', 'post'])
    current_app.register_blueprint(album_blueprint, url_prefix='/api/album')
