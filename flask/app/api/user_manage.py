from flask import jsonify, request, g


def get_user_list():
    from ..models import User
    from ..models import Admin
    page_size = 10
    page = request.args.get('page', 1, type=int)
    name = request.args.get('name', '')
    if g.admin.id != 1:
        users = User.query.filter(User.name.notin_([admin.name for admin in Admin.query.all()]))
    else:
        users = User.query
    if name:
        users = users.filter(
            User.name.like('%{}%'.format(name))).order_by('id')
    else:
        users = users.order_by('id')
    total = users.count()
    if not page:
        users = users.all()
    else:
        users = users.offset((page - 1) * page_size).limit(page_size).all()
    return jsonify({
        'code': 200,
        'total': total,
        'page_size': page_size,
        'infos': [u.to_dict1() for u in users]
    })


def remove_user():
    from .. import db
    from ..models import User as JoinInfos
    remove_id = request.args.get('id', type=int)
    if remove_id:
        remove_info = JoinInfos.query.get(remove_id)
        db.session.delete(remove_info)
        return jsonify({'code': 200, 'msg': "删除成功"})
    else:
        return jsonify({'code': 500, 'msg': "未知错误"})


def batchremove_user():
    from .. import db
    from ..models import User as JoinInfos
    remove_ids = request.args.get('ids').split(',')
    is_current = False
    if remove_ids:
        remove_info = None
        for remove_id in remove_ids:
            remove_info = JoinInfos.query.get(remove_id)
            if remove_info:
                is_current = True
                db.session.delete(remove_info)
            else:
                pass
        print(remove_ids, remove_info)
        if is_current:
            return jsonify({'code': 200, 'msg': "删除成功"})
        else:
            return jsonify({'code': 404, 'msg': "请正确选择"})
    else:
        return jsonify({'code': 500, 'msg': "未知错误"})


def set_user_permit():
    from ..models import User
    set_id = request.args.get('id', type=int)
    if set_id:
        change_user = User.query.get(set_id)
        if change_user.role == 1:
            change_user.lower_permit()
        else:
            change_user.improve_permit()
        return jsonify({'code': 200,
                        'msg': '修改成功',
                        'user_id': set_id,
                        'role': change_user.role
                        })
    else:
        return jsonify({'code': 500, 'msg': "未知错误"})

