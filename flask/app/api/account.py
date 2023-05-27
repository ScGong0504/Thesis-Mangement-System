# 该文件为与用户的账户有关的接口实现函数（这里的“用户”包括了管理员）

import json
import random

from flask import g, jsonify, request, make_response


# 以下为管理员相关函数实现
# 管理员的登录函数实现
def get_auth_token_admin():
    token = g.admin.generate_auth_token()
    return jsonify({'code': 200, 'msg': "登录成功", 'token': token.decode('ascii'), 'name': g.admin.name})


# 管理员的重设密码函数实现
def set_auth_pwd_admin():
    from ..models import Admin
    data = json.loads(str(request.data, encoding="utf-8"))
    admin = Admin.query.filter_by(name=g.admin.name).first()
    if admin and admin.verify_password(data['oldpass']) and data['confirpass'] == data['newpass']:
        admin.hash_password(data['newpass'])
        return jsonify({'code': 200, 'msg': "密码修改成功"})
    else:
        return jsonify({'code': 500, 'msg': "请检查输入"})


# 以下为用户相关函数实现
# 用户的登陆函数实现
def get_auth_token_user():
    token = g.user.generate_auth_token()
    return jsonify({'code': 200, 'msg': "登录成功", 'token': token.decode('ascii'), 'name': g.user.name})


# 用户的注册函数实现
def account_register():
    from ..models import User
    data = json.loads(str(request.data, encoding="utf-8"))
    if name_not_in_db_(data['username']) and data['password'] == data['twicePassword']:
        if User.add(data['username'], data['password'], data['email']):
            return jsonify({'code': 200, 'msg': "注册成功，将跳转至登录页面"})
    return jsonify({'code': 500, 'msg': "注册失败"})


# 用户登录时的名字不重复校验函数实现
def name_not_in_db():
    data = json.loads(str(request.data, encoding="utf-8"))
    if name_not_in_db_(data['username']):
        return jsonify({'code': 200})
    else:
        return jsonify({'code': 500})


# 用户登录时的名字并不重复校验函数的实现——更进一步的
def name_not_in_db_(username):
    from ..models import Admin
    admins = Admin.query.all()
    admins_name = [admin.name for admin in admins]
    if username in admins_name:
        return False
    else:
        return True


# 发送验证码
def get_verify_code():
    from ..util import send_mail
    try:
        data = json.loads(str(request.data, encoding="utf-8"))
        verify_code = str(random.randint(100000, 999999))
        send_mail(data['email'], '【论文管理系统】注册验证码', verify_code)
        return make_response(jsonify({'msg': '验证码发送成功', 'verify_code': verify_code}), 200)
    except Exception as e:
        print('系统错误', e)
        return make_response(jsonify({'msg': '系统错误' + str(e)}), 500)
