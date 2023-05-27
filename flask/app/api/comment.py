from flask import request, g, make_response, jsonify


def get_comment_list(mode='note'):
    from ..models import Comment
    try:
        note_id = request.args.get('note_id', type=int)
        page = request.args.get('page', 1, type=int)
        comment_ = Comment.query
        if note_id is not None:
            if mode == 'my':
                comment_ = comment_.filter_by(comment_user_id=g.user.id)
            elif mode == 'note':
                comment_ = comment_.filter_by(comment_note_id=note_id)
        total = comment_.count()
        page_size = 2
        comments = comment_.order_by('comment_time').offset((page - 1) * page_size).limit(page_size).all()
        return make_response(jsonify({
            'total': total,
            'page_size': page_size,
            'comments': [c.to_dict() for c in comments],
            'msg': '获取评论列表成功',
        }), 200)
    except Exception as e:
        print('系统错误:', str(e))
        return make_response(jsonify({'msg': '系统错误: ' + str(e)}), 500)


def add_comment():
    from ..models import Comment
    try:
        note_id = request.args.get('note_id', type=int)
        comment_content = request.args.get('comment_content')
        Comment.add(comment_content, g.user.id, note_id)
        return make_response(jsonify({
            'msg': '新增评论成功',
        }), 200)
    except Exception as e:
        print('系统错误:', str(e))
        return make_response(jsonify({'msg': '系统错误: ' + str(e)}), 500)


def add_reply():
    from ..models import Reply, PairReply
    try:
        comment_id = request.args.get('comment_id', type=int)
        reply_content = request.args.get('reply_content')
        reply2_id = request.args.get('reply2_id')
        reply = Reply.add(reply_content, g.user.id, comment_id)
        if reply2_id != '':
            PairReply.add(reply.reply_id, int(reply2_id))
        return make_response(jsonify({
            'msg': '新增回复成功',
        }), 200)
    except Exception as e:
        print('系统错误:', str(e))
        return make_response(jsonify({'msg': '系统错误: ' + str(e)}), 500)


def delete_reply():
    from ..models import Reply
    try:
        reply_id = request.args.get('reply_id', type=int)
        reply = Reply.query.get(reply_id)
        if g.user is None or reply.reply_user_id == g.user.id:
            reply.remove()
            return make_response(jsonify({
                'msg': '删除回复成功',
            }), 200)
        else:
            return make_response(jsonify({
                'msg': '您没有删除该回复的权限',
            }), 400)
    except Exception as e:
        print('系统错误:', str(e))
        return make_response(jsonify({'msg': '系统错误: ' + str(e)}), 500)


def delete_comment():
    from ..models import Comment
    try:
        comment_id = request.args.get('comment_id', type=int)
        comment = Comment.query.get(comment_id)
        if g.user is None or comment.comment_user_id == g.user.id:
            comment.remove()
            return make_response(jsonify({
                'msg': '删除回复成功',
            }), 200)
        else:
            return make_response(jsonify({
                'msg': '您没有删除该回复的权限',
            }), 400)
    except Exception as e:
        print('系统错误:', str(e))
        return make_response(jsonify({'msg': '系统错误: ' + str(e)}), 500)
