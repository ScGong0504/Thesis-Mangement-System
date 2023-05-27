from flask import jsonify, request


# 获取所有研究方向
def get_child_domain_list(parent):
    from ..models import ExtendDomain as Extend_domain
    domain_name = parent
    mode = request.args.get('mode', 'admin')
    child_tree = []
    tree = Extend_domain.query.order_by("child_domain").filter_by(parent_domain=domain_name).all()
    if tree:
        for one in tree:
            parent_name = one.child_domain
            grandchild_tree = get_child_domain_list(parent_name)
            if mode == 'user':
                child_dic = {"label": parent_name, "children": grandchild_tree, 'value': parent_name}
            else:
                child_dic = {"label": parent_name, "children": grandchild_tree}
            child_tree.append(child_dic)
        return child_tree
    else:
        return child_tree


def get_domain_list():
    try:
        _tree = get_domain_list_()
        return jsonify({
            'tree': _tree,
            'code': 200,
            'msg': "获取成功"
        })
    except Exception as e:
        print("系统错误")
        return jsonify({
            'code': 500,
            'msg': "获取失败"
        })


# 增加研究方向
def add_domain_list():
    from .. import db
    from ..models import Domain
    from ..models import ExtendDomain as Extend_domain
    try:
        domain_name = request.args.get('domain_name')
        parent_domain = request.args.get('parent_domain')
        if domain_name and parent_domain:
            existed_domain_names = Domain.query.all()
            # 如果名称已存在 domain表不可能为空 有第0层
            # if existed_domain_names:
            for existed_domain_name in existed_domain_names:
                if domain_name == existed_domain_name.domain_name and existed_domain_name.is_deleted == 0:
                    return jsonify({
                        'code': 500,
                        'msg': '该研究方向名称已存在,请重新设置'
                    })
                # 若是曾经某个父节点下的某个已删除子节点（联系表中应该无此父子节点关系），改is_deleted，增加一条数据到联系表中即可
                if domain_name == existed_domain_name.domain_name and existed_domain_name.is_deleted == 1:
                    existed_domain_name.is_deleted = 0
                    e_domain = Extend_domain()
                    e_domain.parent_domain = parent_domain
                    e_domain.child_domain = domain_name
                    db.session.add(e_domain)
                    db.session.commit()
                    return jsonify({
                        'code': 200,
                        'msg': "增加成功"
                    })

            # domain_name是全新的 加入domain表，建立联系
            # 其实如果没有可以浏览研究方向的设置的历史记录的 没必要搞级联删除？
            new_domain = Domain()
            new_domain.domain_name = domain_name
            new_domain.is_deleted = 0
            db.session.add(new_domain)
            db.session.commit()
            e_domain = Extend_domain()
            e_domain.parent_domain = parent_domain
            e_domain.child_domain = domain_name
            db.session.add(e_domain)
            db.session.commit()
            return jsonify({
                'code': 200,
                'msg': "增加成功"
            })
        else:
            return jsonify({
                'code': 500,
                'msg': "输入为空，增加失败"
            })
    except Exception as e:
        print("系统错误")
        return jsonify({
            'code': 500,
            'msg': "添加失败"
        })


# 删除研究方向
def delete_domain():
    from .. import db
    from ..models import Domain
    from ..models import ExtendDomain as Extend_domain
    try:
        domain_name = request.args.get('domain_name')
        parent_domain = request.args.get('parent_domain')
        existed_domain_names = Domain.query.all()
        for existed_domain_name in existed_domain_names:
            if domain_name == existed_domain_name.domain_name:
                if existed_domain_name.is_deleted == 0:
                    existed_domain_name.is_deleted = 1  # 逻辑删除
                    db.session.commit()
                    break
                else:
                    return jsonify({
                        'code': 500,
                        'msg': "删除失败"
                    })
            else:
                pass  # 不存在不在列表中还能删除的情况
        # 判断是否有子方向
        is_sons = Extend_domain.query.filter_by(parent_domain=domain_name).all()
        if is_sons:
            # print("有子方向")
            # 有子方向 将子方向的parent_domain改为domain_name的parent_domain
            for is_son in is_sons:
                is_son.parent_domain = parent_domain
            need_deleted = Extend_domain.query.filter_by(child_domain=domain_name).first()
            db.session.delete(need_deleted)
            db.session.commit()
            return jsonify({
                'code': 200,
                'msg': "删除成功"
            })
        # 没有子方向 extend_domain表里有他吗 没有 删除作为domain_name作为子节点的联系数据
        else:
            need_deleted = Extend_domain.query.filter_by(child_domain=domain_name).first()
            db.session.delete(need_deleted)
            db.session.commit()
            return jsonify({
                'code': 200,
                'msg': "删除成功"
            })
    except Exception as e:
        print("系统错误")
        return jsonify({
            'code': 500,
            'msg': "删除失败"
        })


# 修改研究方向名称
def update_domain():
    from .. import db
    from ..models import Domain
    from ..models import ExtendDomain as Extend_domain
    try:
        domain_name = request.args.get('domain_name')
        new_domain = request.args.get('new_name')
        if new_domain == domain_name:
            return jsonify({
                'code': 500,
                'msg': "修改无效"
            })
        else:
            need = Domain.query.filter_by(domain_name=domain_name).first()
            existed = Domain.query.filter_by(domain_name=new_domain).first()
            if existed:
                if existed.is_deleted == 0:
                    return jsonify({
                        'code': 500,
                        'msg': "修改失败，新名称已存在"
                    })
                elif existed.is_deleted == 1:
                    existed.is_deleted = 0
                    need_2 = Extend_domain.query.filter_by(parent_domain=domain_name).all()
                    for one in need_2:
                        one.parent_domain = new_domain
                    need_3 = Extend_domain.query.filter_by(child_domain=domain_name).all()
                    for one in need_3:
                        one.child_domain = new_domain
                    db.session.delete(need)
                    db.session.commit()
                    return jsonify({
                        'code': 200,
                        'msg': "修改成功"
                    })
            else:
                new_d = Domain(domain_name=new_domain, is_deleted=0)
                db.session.add(new_d)
                db.session.commit()
                need_2 = Extend_domain.query.filter_by(parent_domain=domain_name).all()
                for one in need_2:
                    one.parent_domain = new_domain
                need_3 = Extend_domain.query.filter_by(child_domain=domain_name).all()
                for one in need_3:
                    one.child_domain = new_domain
                db.session.delete(need)
                db.session.commit()
                return jsonify({
                    'code': 200,
                    'msg': "修改成功"
                })
    except Exception as e:
        print("系统错误")
        return jsonify({
            'code': 500,
            'msg': "失败"
        })


def get_domain_list_():
    from ..models import ExtendDomain
    _tree = []
    root_dic = {}
    domain_name = 'grandfather'
    mode = request.args.get('mode', 'admin')
    if mode == 'user':
        root_dic["label"] = domain_name
        root_dic["value"] = domain_name
    else:
        root_dic["label"] = domain_name
    first_tree = ExtendDomain.query.order_by("child_domain").filter_by(parent_domain=domain_name).all()
    if first_tree:
        for one in first_tree:
            children = get_child_domain_list(one.child_domain)
            if mode == 'user':
                child_dic = {"label": one.child_domain, "children": children, "value": one.child_domain}
            else:
                child_dic = {"label": one.child_domain, "children": children}
            _tree.append(child_dic)
    else:
        pass
    return _tree
