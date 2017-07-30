# coding=utf-8
from flask import g
from request_service import load_admin, load_user


def admin_required(f):
    from backend_common.models.admin import Admin as AdminModel

    @load_admin
    def decorator(*args, **kwargs):
        if kwargs.get('admin'):
            return f(*args, **kwargs)
        raise AdminModel.NotAuthError()
    return decorator


def user_required(f):
    from backend_common.models.user import User as UserModel

    @load_user
    def decorator(*args, **kwargs):
        if kwargs.get('user'):
            return f(*args, **kwargs)
        raise UserModel.NotAuthError()
    return decorator
