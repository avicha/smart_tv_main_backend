# coding=utf-8

from controllers.tv import tv_blueprint, TVController
from controllers.user import user_blueprint, UserController
from controllers.category import category_blueprint, CategoryController
from controllers.common import common_blueprint, CommonController
from controllers.video import video_blueprint, VideoController


def init_app(current_app):
    tv_blueprint.add_url_rule('/get_search_options', 'get_search_options_api', TVController.get_search_options, methods=['get'])
    tv_blueprint.add_url_rule('/search', 'search_api', TVController.search, methods=['get', 'post'])
    tv_blueprint.add_url_rule('/get_detail', 'get_detail_api', TVController.get_detail, methods=['get'])
    tv_blueprint.add_url_rule('/get_parts', 'get_parts_api', TVController.get_parts, methods=['get'])
    current_app.register_blueprint(tv_blueprint, url_prefix='/api/tv')

    user_blueprint.add_url_rule('/status', 'status_api', UserController.status, methods=['get'])
    current_app.register_blueprint(user_blueprint, url_prefix='/api/user')

    # category_blueprint.add_url_rule('/create', 'create_api', CategoryController.create, methods=['get'])
    category_blueprint.add_url_rule('/list', 'list_api', CategoryController.list, methods=['get'])
    current_app.register_blueprint(category_blueprint, url_prefix='/api/category')

    common_blueprint.add_url_rule('/now', 'now_api', CommonController.now, methods=['get'])
    common_blueprint.add_url_rule('/weather', 'weather_api', CommonController.weather, methods=['get'])
    current_app.register_blueprint(common_blueprint, url_prefix='/api/common')

    video_blueprint.add_url_rule('/get_play_info', 'get_play_info_api', VideoController.get_play_info, methods=['get'])
    current_app.register_blueprint(video_blueprint, url_prefix='/api/video')
