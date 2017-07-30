# coding=utf-8
from flask import request, current_app
from backend_common.services.utils import dict_utils


def get_request_params(*fields, **opts):
    def _get_request_params(f):
        def decorator(*args, **kwargs):
            data = request.json or request.form or request.args
            if fields:
                kwargs.update({'data': dict_utils.pick(data, *fields, **opts)})
            else:
                kwargs.update({'data': data})
            return f(*args, **kwargs)
        return decorator
    return _get_request_params


def load_admin(f):
    def decorator(*args, **kwargs):
        from flask import request,  current_app
        from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature
        from backend_common.models.admin import Admin as AdminModel
        data = request.json or request.form or request.args
        if data.get('token'):
            token = data.get('token')
            s = TimedJSONWebSignatureSerializer(current_app.secret_key)
            try:
                user_id = s.loads(token)
                admin = AdminModel.get(AdminModel.id == user_id, AdminModel.deleted_at == None)
                tokens = admin.tokens()
                if token in tokens:
                    kwargs.update({'admin': admin})
                    return f(*args, **kwargs)
                else:
                    raise AdminModel.TokenError(u'请重新登录')
            except SignatureExpired:
                raise AdminModel.TokenError(u'登录已经过期')
            except BadSignature:
                raise AdminModel.PasswordError()
            except AdminModel.DoesNotExist, e:
                raise AdminModel.NotFoundError(u'该用户不存在')
        else:
            kwargs.update({'admin': None})
            return f(*args, **kwargs)
    return decorator


def load_user(f):
    def decorator(*args, **kwargs):
        from flask import request, current_app
        from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature
        from backend_common.models.user import User as UserModel
        data = request.json or request.form or request.args
        if data.get('token'):
            token = data.get('token')
            s = TimedJSONWebSignatureSerializer(current_app.secret_key)
            try:
                user_id = s.loads(token)
                user = UserModel.get(UserModel.id == user_id, UserModel.deleted_at == None)
                tokens = user.tokens()
                if token in tokens:
                    kwargs.update({'user': user})
                    return f(*args, **kwargs)
                else:
                    raise UserModel.TokenError(u'请重新登录')
            except SignatureExpired:
                raise UserModel.TokenError(u'登录已经过期')
            except BadSignature:
                raise UserModel.TokenError(u'登录Token信息错误')
            except UserModel.DoesNotExist, e:
                raise UserModel.NotFoundError(u'该用户不存在')
        else:
            kwargs.update({'user': None})
            return f(*args, **kwargs)
    return decorator
