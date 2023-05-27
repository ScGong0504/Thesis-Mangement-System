from flask import make_response, jsonify, request, g
from sqlalchemy import or_


# 测试模板
def query_papers(mode='all'):
    from ..models import User, Paper, Meeting, Author, PaperAuthor, PaperDomain, PaperUser
    # try:
    # 参数获取对应查询
    page = request.args.get('page', 1, type=int)
    condition_join = request.args.get('condition_join', 'and')
    query_args = paper_query_arg(condition_join)
    # 查询结果
    condition = '{}, {}, {}, {}, {}, {}, {}'.format(
        query_args['title'], query_args['author'], query_args['user'],
        query_args['meeting'], query_args['abstract'], query_args['paper_type'],
        query_args['domain']
    )
    # 默认为查询所有模式
    if mode == 'my':
        condition += ', Paper.paper_account_id==g.user.id'
    # 默认为and连接条件
    if condition_join == 'or':
        condition = 'or_(' + condition + ')'
    papers_q = eval('Paper.query.filter({}).order_by(Paper.id)'.format(condition))
    # 设置返回格式
    total = papers_q.count()
    page_size = 6
    papers = papers_q.offset((page - 1) * page_size).limit(page_size).all()
    # 正确的返回结果
    return make_response(jsonify({
        'total': total,
        'page_size': page_size,
        'infos': [p.to_dict() for p in papers],
        'msg': '更新获取论文列表成功',
    }), 200)
    # except Exception as e:
    #     print('系统错误:', e)
    #     return make_response(jsonify({'msg': '！更新获取论文列表失败！系统错误: ' + str(e)}), 500)


def paper_query_arg(condition_join):
    arg_keys = ('title', 'author', 'user', 'meeting', 'abstract', 'paper_type', 'domain')
    query_args = {}
    for arg_key in arg_keys:
        arg_value = request.args.get(arg_key, '')
        # 若为空则返回一个筛选所有值的条件
        if arg_value == '':
            if condition_join == 'and':
                query_args[arg_key] = 'Paper.id!=0'
            else:
                query_args[arg_key] = 'Paper.id==0'
            continue
        # 第一个元素为筛选条件值 第二个为是否取反（1取反，0不取反_默认） 第三个为是否模糊查询（若有）（1模糊查询，0精确查询_默认）
        arg_value_ = arg_value.split('|')
        for i in range(3 - len(arg_value_)):
            arg_value_.append('0')
        # 实现
        if arg_key == 'paper_type':
            result = 'Paper.type=="{}"'.format(arg_value[0])
        elif arg_key == 'user':
            if arg_value_[2] == '0':
                result = 'Paper.paper_account_id.in_([u.id for u in User.query.filter' \
                         '(User.name=="{}")])'.format(arg_value_[0])
            else:
                result = 'Paper.paper_account_id.in_([u.id for u in User.query.filter' \
                         '(User.name.like("{}"))])'.format('%' + arg_value_[0] + '%')
        elif arg_key == 'meeting':
            if arg_value_[2] == '0':
                result = 'Paper.paper_meeting_id.in_([m.id for m in Meeting.query.filter' \
                         '(Meeting.meeting_title=="{}")])'.format(arg_value_[0])
            else:
                result = 'Paper.paper_meeting_id.in_([m.id for m in Meeting.query.filter' \
                         '(Meeting.meeting_title.like("{}"))])'.format('%' + arg_value_[0] + '%')
        elif arg_key == 'domain':
            if arg_value_[2] == '0':
                result = 'Paper.id.in_([pd.paper_id for pd in PaperDomain.query.filter' \
                         '(PaperDomain.domain_name=="{}")])'.format(arg_value_[0])
            else:
                result = 'Paper.id.in_([pd.paper_id for pd in PaperDomain.query.filter' \
                         '(PaperDomain.domain_name.like("%{}%"))])'.format('%' + arg_value_[0] + '%')
        elif arg_key == 'author':
            if arg_value_[2] == '0':
                result = 'Paper.id.in_([pa.paper_id for pa in PaperAuthor.query.filter' \
                         '(PaperAuthor.author_id.in_([a.id for a in Author.query.filter' \
                         '(Author.name=="{}").all()]))])'.format(arg_value_[0])
            else:
                result = 'Paper.id.in_([pa.paper_id for pa in PaperAuthor.query.filter' \
                         '(PaperAuthor.author_id.in_([a.id for a in Author.query.filter' \
                         '(Author.name.like("{}")).all()]))])'.format('%' + arg_value_[0] + '%')
        else:
            if arg_value_[2] == '0':
                result = 'Paper.{}=="{}"'.format(arg_key, arg_value_[0])
            else:
                result = 'Paper.{}.like("%{}%")'.format(arg_key, arg_value_[0])
        if arg_value_[1] == '1':
            result = '~{}'.format(result)
        query_args[arg_key] = result
    return query_args


def query_lot_paper_by_titles():
    from ..models import Paper
    try:
        titles = request.args.get('titles').split()
        page = request.args.get('page', 1, type=int)
        papers_q = Paper.query
        for title in titles:
            papers_q = papers_q.filter(Paper.title.notlike('%{}%'.format(title)))
        papers = papers_q.distinct().all()
        papers_q = Paper.query.filter(Paper.id.notin_([p.id for p in papers]))
        total = papers_q.count()
        page_size = 6
        papers = papers_q.offset((page - 1) * page_size).limit(page_size).all()
        return make_response(jsonify({
            'total': total,
            'page_size': page_size,
            'infos': [p.to_dict() for p in papers],
            'msg': '更新获取论文列表成功',
        }), 200)
    except Exception as e:
        print('系统错误:', e)
        return make_response(jsonify({'msg': '！更新获取论文列表失败！系统错误: ' + str(e)}), 500)
