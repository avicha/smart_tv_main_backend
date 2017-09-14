# coding=utf-8
from controllers.singer import singer_blueprint, SingerController
from controllers.album import album_blueprint, AlbumController
from controllers.song import song_blueprint, SongController
from controllers.tv import tv_blueprint, TVController
from controllers.user import user_blueprint, UserController
from controllers.category import category_blueprint, CategoryController
from controllers.common import common_blueprint, CommonController


def init_app(current_app):
    singer_blueprint.add_url_rule('/search', 'search_api', SingerController.search, methods=['get', 'post'])
    current_app.register_blueprint(singer_blueprint, url_prefix='/api/singer')

    album_blueprint.add_url_rule('/search', 'search_api', AlbumController.search, methods=['get', 'post'])
    current_app.register_blueprint(album_blueprint, url_prefix='/api/album')

    song_blueprint.add_url_rule('/search', 'search_api', SongController.search, methods=['get', 'post'])
    current_app.register_blueprint(song_blueprint, url_prefix='/api/song')

    tv_blueprint.add_url_rule('/search', 'search_api', TVController.search, methods=['get', 'post'])
    current_app.register_blueprint(tv_blueprint, url_prefix='/api/tv')

    user_blueprint.add_url_rule('/status', 'status_api', UserController.status, methods=['get'])
    current_app.register_blueprint(user_blueprint, url_prefix='/api/user')

    # category_blueprint.add_url_rule('/create', 'create_api', CategoryController.create, methods=['get'])
    category_blueprint.add_url_rule('/list', 'list_api', CategoryController.list, methods=['get'])
    current_app.register_blueprint(category_blueprint, url_prefix='/api/category')

    common_blueprint.add_url_rule('/now', 'now_api', CommonController.now, methods=['get'])
    common_blueprint.add_url_rule('/weather', 'weather_api', CommonController.weather, methods=['get'])
    current_app.register_blueprint(common_blueprint, url_prefix='/api/common')
