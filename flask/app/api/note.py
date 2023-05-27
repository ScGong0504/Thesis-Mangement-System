from flask import request, g, make_response, jsonify


def get_note_list():
    from ..models import Note
    try:
        paper_id = request.args.get('paper_id', '')
        page = request.args.get('page', 1, type=int)
        note_q = Note.query.filter_by(note_paper_id=paper_id)
        total = note_q.count()
        page_size = 3
        notes = note_q.offset((page - 1) * page_size).limit(page_size).all()
        return make_response(jsonify({
            'total': total,
            'page_size': page_size,
            'notes': [n.to_dict() for n in notes],
            'msg': '获取笔记成功'
        }), 200)
    except Exception as e:
        print('系统错误:', e)
        return make_response(jsonify({'msg': '系统错误: ' + str(e)}), 500)


def add_note():
    from ..models import Note
    try:
        if can_i_add_note_():
            new_note_title = request.args.get('new_note_title')
            new_note_content = request.args.get('new_note_content')
            Note.add(new_note_content, request.args.get('paper_id'), new_note_title)
            return make_response(jsonify({'msg': '新增笔记成功'}), 200)
        else:
            return make_response(jsonify({'msg': '权限错误: 您不可以创建一个新的笔记在该论文下'}), 400)
    except Exception as e:
        print('系统错误:', e)
        return make_response(jsonify({'msg': '系统错误: ' + str(e)}), 500)


def can_i_add_note():
    if can_i_add_note_():
        return make_response(jsonify({'msg': 'ok!'}), 200)
    else:
        return make_response(jsonify({'msg': 'error!'}), 500)


def can_i_add_note_():
    from ..models import Paper
    paper_id = request.args.get('paper_id', '')
    paper = Paper.query.get(paper_id)
    if paper.paper_account_id == g.user.id:
        return True
    else:
        return False


def delete_note():
    from ..models import Note
    try:
        note_id = request.args.get('note_id', 0, type=int)
        if can_i_add_note_():
            note = Note.query.get(note_id)
            note.remove()
        return make_response(jsonify({
            'msg': '删除笔记成功',
        }), 200)
    except Exception as e:
        print('系统错误:', str(e))
        return make_response(jsonify({'msg': '系统错误: ' + str(e)}), 500)
