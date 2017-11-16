# coding=utf-8
from flask import Blueprint
from backend_common.controllers.base import BaseController
from backend_common.middlewares.request_service import get_request_params
from backend_common.models.mongodb import db

from backend_common.services.crawler.youku import get_play_info
import backend_common.const.video_source as video_source
import time

video_blueprint = Blueprint('video', __name__)


class VideoController(BaseController):

    @classmethod
    @get_request_params()
    def get_play_info(cls, data):
        video_id = data.get('video_id')
        source = int(data.get('source'))
        if source is video_source.YOUKU:
            result = get_play_info(video_id)
            return cls.success_with_result(result)
