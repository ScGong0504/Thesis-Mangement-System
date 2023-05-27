from flask import jsonify, request, json, g


# 遍历获得domain父节点
def get_paper_parent_domain(parent, child_domain_name):
    from ..models import ExtendDomain as Extend_domain
    parent.append(child_domain_name)
    # print(parent)
    parent_domain = Extend_domain.query.filter_by(child_domain=child_domain_name).first()
    if parent_domain:
        parent_domain_name = parent_domain.parent_domain
        # print(parent_domain_name)
        if parent_domain_name == 'grandfather':
            return parent
        else:
            get_paper_parent_domain(parent, parent_domain_name)
            return parent
    else:
        return parent


# 遍历获得domain子节点 children 为list
def get_paper_child_domain(children, parent_domain_name):
    from ..models import ExtendDomain as Extend_domain
    child_domain_name = Extend_domain.query.filter_by(parent_domain=parent_domain_name).first()
    if child_domain_name:
        child_domain_name = child_domain_name.child_domain
        children.append(child_domain_name)
        get_paper_child_domain(child_domain_name)
        return children
    else:
        return children


# 将paper_title转换程中文名
def type_trans(type):
    if type == 1:
        type_name = "理论证明型"
    elif type == 2:
        type_name = "综述型"
    elif type == 3:
        type_name = "实验型"
    elif type == 4:
        type_name = "工具型"
    elif type == 5:
        type_name = "数据集型"
    else:
        type_name = ""
    return type_name


def paper_details():
    from ..models import Paper as paper
    from ..models import Author, PaperAuthor as Paper_author, PaperDomain as Paper_domain, Cite
    from ..models import Document, Meeting, Note
    try:
        # print("---1、enter try---")
        paper_id = request.args.get('paper_id', type=int)
        # print(paper_id)
        paper_choose = paper.query.filter_by(id=paper_id).first()
        # print("---2、get paper success---")
        # print(paper_choose)
        title = paper_choose.title
        # print("---3、get paper title success---")
        abstract = paper_choose.abstract
        # print("---4、get paper abstract success---",abstract)
        author_id = Paper_author.query.order_by("level").filter_by(paper_id=paper_id).all()
        # print("---5、get author",author_id)
        author = []
        for one in author_id:
            a_id = one.author_id
            author_name = Author.query.filter_by(id=a_id).first()
            author.append(author_name.name)
        # print(author)
        cited_papers = Cite.query.filter_by(citing_paper=paper_id).all()
        paper_cited_issue = []
        if cited_papers:
            for one in cited_papers:
                one_title = paper.query.filter_by(id=one.cited_paper).first().title
                paper_cited_issue.append({'paper_id': one.cited_paper, 'title': one_title})
        else:
            paper_cited_issue = None
        # print("----paper_cited_issue",paper_cited_issue)
        paper_body_issue = paper_choose.body_url
        paper_meeting = paper_choose.paper_meeting_id
        # print("paper_body_issue:", paper_body_issue,  "paper_meeting", paper_meeting)
        paper_meeting_name = Meeting.query.filter_by(id=paper_meeting).first().meeting_title
        # print("---paper_meeting_name:",paper_meeting_name)
        # print(paper_choose)
        paper_publish_time = paper_choose.issue_date
        paper_send_time = paper_choose.publish_time
        # print("-----")
        paper_type = paper_choose.type
        # print(type(paper_type))
        # print(type_trans(paper_type))
        paper_document = Document.query.filter_by(doucument_paper_id=paper_id).first()
        # print(paper_document)
        if not paper_document:
            paper_document = None
        else:
            paper_document = paper_document.document_url
        domain_name = Paper_domain.query.filter_by(paper_id=paper_id).first().domain_name
        # print(domain_name)
        paper_parent_domains = []
        paper_child_domains = []
        paper_domain_name = get_paper_parent_domain(paper_parent_domains, domain_name) + get_paper_child_domain(
            paper_child_domains, domain_name)
        note = Note.query.filter_by(note_paper_id=paper_id).first()
        if note:
            note_id = note.note_id
        else:
            note_id = None
        return jsonify({
            'code': 200,
            'msg': '显示成功',
            'paperInfos': {
                'title': title,
                'author': author,
                'abstract': abstract,
                'paper_type': type_trans(paper_type),
                'paper_domain_name': paper_domain_name,
                'paper_publish_time': paper_publish_time,
                'paper_send_time': paper_send_time,
                'paper_meeting_name': paper_meeting_name,
                'note_id': note_id,
                'paper_body_url': paper_body_issue,
                'cited_paper': paper_cited_issue,
                'paper_document': paper_document
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': '未知错误'
        })


def get_mypaper_list():
    from ..models import Paper
    from ..models import PaperUser as Paper_user
    # 没有用户对应的paper表》》》
    # try:
    page_size = 6
    page = request.args.get('page', 1, type=int)
    # print("----进入try---",page)
    user_id = g.user.id
    # print("----进入try---",user_id)
    user_papers = Paper_user.query.order_by(Paper_user.paper_id.desc()).filter_by(user_id=user_id)
    # print("----",type(user_papers))
    user_papers_count = user_papers.all()
    total = 0
    for one in user_papers_count:
        total += 1
    total_page = int(total / page_size)
    if total - total_page * page_size:
        total_page += 1
    # print("-----",type(user_papers_count))
    # print(user_papers)
    user_papers = user_papers.offset((page - 1) * page_size).limit(page_size).all()
    # print(user_papers)
    paperInfos = []
    for one in user_papers:
        paper = Paper.query.filter_by(id=one.paper_id).first()
        paperList = {}
        paperList.update({'paper_id': paper.id})
        paperList.update({'paper_title': paper.title})
        paperList.update({'paper_send_time': paper.publish_time})
        paperList.update({'paper_type': type_trans(paper.type)})
        paperInfos.append(paperList)
    if paperInfos:
        return jsonify({
            'code': 200,
            'msg': "获取成功",
            'total': total,
            'total_page': total_page,
            'page_size': page_size,
            'paperInfos': paperInfos
        })
    else:
        return jsonify({
            'code': 200,
            'msg': "获取成功,未曾发布过论文"
        })
    # except Exception as e:
    #     print("系统错误")
    #     return jsonify({
    #         'code': 500,
    #         'msg': "失败"
    #     })


# 论文发布
def post_paper():
    from .. import db
    from ..models import Paper, Domain, Author, PaperAuthor as Paper_author
    from ..models import PaperUser as Paper_user, Meeting, Cite, Note, Document
    from ..models import PaperDomain as Paper_domain, ExtendDomain as Extend_domain
    try:
        print("1")
        user_id = g.user.id
        print(user_id)
        paper_title = request.args.get('paper_title')
        print(paper_title)
        paper_first_author = request.args.get('paper_first_author')
        print(paper_first_author)
        first_author_email = request.args.get('first_author_email')
        print(first_author_email)
        paper_second_author = request.args.get('paper_second_author')
        second_author_email = request.args.get('second_author_email')
        paper_third_author = request.args.get('paper_third_author')
        third_author_email = request.args.get('third_author_email')
        paper_abstract = request.args.get('paper_abstract')
        print(paper_abstract)
        paper_type = request.args.get('paper_type', type=int)
        print(paper_type)
        paper_publish_time = request.args.get('paper_publish_time')
        print(paper_publish_time)
        paper_send_time = request.args.get('paper_send_time')
        print(paper_send_time)
        meeting = request.args.get('meeting')
        cited_paper = json.loads(request.args.get('cited_paper'))  # list传参出现问题
        print(cited_paper)
        body_url = request.args.get('body_url')
        print(body_url)
        note = request.args.get('note')
        print(note)
        domain_name = request.args.get('domain_name')  # 传最后一个节点
        print(domain_name)
        document_url = request.args.get('document_url')  # 附加文件
        print(document_url)
        print("传参success")
        is_meeting_existed = Meeting.query.filter_by(meeting_title=meeting).first()
        if is_meeting_existed:
            meeting_id = is_meeting_existed.id
        else:
            Meeting.add(meeting, None, None)
            meeting_id = Meeting.query.filter_by(meeting_title=meeting).first().id
        print("----meeting实现----")
        is_paper_existed = Paper.query.filter_by(title=paper_title).first()
        # 如果论文标题已存在，改为更新标题
        if is_paper_existed:
            print("更新论文内容")
            is_paper_existed.title = paper_title
            is_paper_existed.publish_time = paper_send_time
            is_paper_existed.abstract = paper_abstract
            is_paper_existed.type = paper_type
            is_paper_existed.issue_date = paper_publish_time
            is_paper_existed.body_url = body_url
            is_paper_existed.paper_account_id = user_id
            is_paper_existed.paper_meeting_id = meeting_id
            db.session.commit()
            paper_id = is_paper_existed.id
        # Paper_user.add(user_id, is_paper_existed.id)
        else:
            Paper.add(paper_title, paper_send_time, paper_abstract, paper_type, paper_publish_time, body_url, user_id,
                      meeting_id)
            print("---增加成功---")
            paper_id = Paper.query.filter_by(title=paper_title).first().id
            print(paper_id)
            Paper_user.add(user_id, paper_id)
            # 关于多个用户上传同一篇论文
        # 处理附加文件
        if document_url:
            Document.add(document_url, "附加文件", paper_id)  # document_name 设为附件文件
        print(type(cited_paper))
        # list问题
        for one in cited_paper:
            print(one)
            cited_paper_id = Paper.query.filter_by(title=one).first()
            if cited_paper_id:
                cited_paper_id = cited_paper_id.id
                # paper_id 是新增的 所以不用判断引用关系是否存在
                Cite.add(paper_id, cited_paper_id)
            else:
                return jsonify({
                    'code': 500,
                    'msg': "引用论文不在系统中，请重新选择"
                })
        ###
        if note:
            Note.add(note, paper_id)
        else:
            pass
        # 处理domain_name
        domain = []
        domain_tree = get_paper_parent_domain(domain, domain_name)
        print("domain_tree：", domain_tree)
        for one in domain_tree:
            Paper_domain.add(paper_id, one)
        # 改进 传参时，author以list[{"name":  ,"email": },{}]按照一二级作者顺序传入 这里只考虑吧每一级只有一位作者 若多位，改成[[{}].[{}]]
        if paper_first_author:
            is_exited = Author.query.filter(
                Author.name == paper_first_author and Author.email == first_author_email).first()
            if is_exited:
                pass
            else:
                Author.add(paper_first_author, first_author_email, '')
            author_id = Author.query.filter(
                Author.name == paper_first_author and Author.email == first_author_email).first().id
            Paper_author.add(paper_id, author_id, 1)
        if paper_second_author:
            is_exited = Author.query.filter(
                Author.name == paper_second_author and Author.email == second_author_email).first()
            if is_exited:
                pass
            else:
                Author.add(paper_second_author, second_author_email, '')
            author_id_2 = Author.query.filter(
                Author.name == paper_second_author and Author.email == second_author_email).first().id
            Paper_author.add(paper_id, author_id_2, 2)
        if paper_third_author:
            is_exited = Author.query.filter(
                Author.name == paper_third_author and Author.email == third_author_email).first()
            if is_exited:
                pass
            else:
                Author.add(paper_third_author, third_author_email, '')
            author_id_3 = Author.query.filter(
                Author.name == paper_third_author and Author.email == third_author_email).first().id
            Paper_author.add(paper_id, author_id_3, 3)
        return jsonify({
            'code': 200,
            'msg': "发布成功"
        })
    except Exception as e:
        print("系统错误")
        return jsonify({
            'code': 500,
            'msg': "发布失败"
        })


# 修改论文
def update_paper():
    from .. import db
    from ..models import Paper, Author, PaperAuthor as Paper_author
    from ..models import Meeting, Cite, Note
    from ..models import PaperDomain as Paper_domain, Document
    paper_id = request.args.get('paper_id')
    paper_title = request.args.get('paper_title')
    paper_first_author = request.args.get('paper_first_author')
    first_email_author = request.args.get('first_email_author')
    paper_second_author = request.args.get('paper_second_author')
    second_email_author = request.args.get('second_email_author')
    paper_third_author = request.args.get('paper_third_author')
    third_email_author = request.args.get('third_email_author')
    paper_abstract = request.args.get('paper_abstract')
    paper_publish_time = request.args.get('paper_publish_time')
    paper_send_time = request.args.get('paper_publish_time')
    meeting = request.args.get('meeting')
    cited_paper = request.args.get('cited_paper', type=list)
    body_url = request.args.get('body_url')
    document_url = request.args.get('document_url')
    note = request.args.get('note')
    domain_name = request.args.get('domain_name')
    paper_type = request.args.get('paper_type', type=int)
    existed_paper = Paper.query.filter_by(id=paper_id).first()
    if g.user.id != existed_paper.paper_account_id:
        return jsonify({
            'code': 500,
            'msg': "当前权限错误，不能修改论文"
        })
    if existed_paper:
        existed_paper.title = paper_title
        existed_paper.type = paper_type
        existed_paper.abstract = paper_abstract
        existed_paper.issue_date = paper_publish_time
        existed_paper.publish_time = paper_send_time
        existed_paper.body_url = body_url
        existed_meeting_id = existed_paper.paper_meeting_id
        existed_meeting_name = Meeting.query.filter_by(id=existed_meeting_id).first().meeting_title
        # is_meeting_existed = Meeting.query.filter_by(meeting_title=meeting).first()
        if existed_meeting_name == meeting:
            pass
        else:
            # 更新paper_meeting_id的外键即可
            Meeting.add(meeting, None, None)
            new_meeting_id = Meeting.query.filter_by(meeting_title=meeting).first().id
            existed_paper.paper_meeting_id = new_meeting_id
        # 处理作者
        paper_authors = Paper_author.query.order_by("level").filter_by(paper_id=paper_id).all()
        print(paper_authors)
        authors = [[paper_first_author, first_email_author], [paper_second_author, second_email_author],
                   [paper_third_author, third_email_author]]
        print("authors____", authors)
        i = 0
        while i < len(paper_authors):
            author = Author.query.filter_by(id=paper_authors[i].author_id).first()
            author_name = author.name
            author_email = author.email
            if authors[i]:
                if author_name != authors[i][0] or author_email != authors[i][1]:
                    Author.add(authors[i][0], authors[i][1], None)
                    author_new_id = Author.query.filter(Author.name == authors[i][0],
                                                        Author.email == authors[i][1]).first().id
                    Paper_author.add(paper_id, author_new_id, i)
                    # 做了修改后 删除原有联系条目，但meeting保留
                    db.session.delete(paper_authors[i])
                    db.session.commit()
            i += 1
        # 处理附加文件
        document_old = Document.query.filter_by(doucument_paper_id=existed_paper.id).first()
        if document_old:
            if document_old.document_url != document_url:
                document_old.document_url = document_url
        else:
            Document.add(document_url, '附加文件', existed_paper.id)
        # 处理cite的修改  删除原来的 加上现在的
        j = 0
        cite = Cite.query.filter_by(citing_paper=existed_paper.id).all()
        cited_paper_id = []
        print(len(cited_paper_id))
        while j < len(cited_paper_id):
            cite_id = Paper.query.filter_by(title=cited_paper[j]).first().id
            if cite_id:
                cited_paper_id.append(cite_id)
                j += 1
                continue
            else:
                return jsonify({
                    'code': 500,
                    'msg': "被引用论文不在系统中"
                })
        for one in cite:
            db.session.delete(one)
        for one in cited_paper_id:
            Cite.add(existed_paper.id, one)

        # 处理domain 传入的是修改后的子节点
        new_domain = [domain_name]
        new_domains = [get_paper_parent_domain(new_domain, domain_name)]
        print("new_domain:", new_domains)
        old_domains = Paper_domain.query.filter_by(paper_id=existed_paper.id).all()
        print(old_domains)
        i = 0
        for one in old_domains:
            one.domain_name = new_domains[0][i]
            i += 1
        db.session.commit()
        old_note = Note.query.filter_by(note_paper_id=existed_paper.id).first()
        print("old_note:", old_note)
        print("note:", note)
        if old_note:
            old_note.note_comment = note
        else:
            Note.add(note, existed_paper.id)
        db.session.commit()
        return jsonify({
            'code': 200,
            'msg': "成功"
        })
    else:
        print("系统错误，paper_id 不符合")
        return jsonify({
            'code': 500,
            'msg': "失败"
        })


# 删除论文
def delete_paper(mode='admin'):
    from .. import db
    from ..models import Paper, PaperAuthor as Paper_author
    from ..models import PaperUser as Paper_user, Cite, Note
    from ..models import PaperDomain as Paper_domain, Document
    try:
        paper_id = request.args.get('paper_id')
        print("paper_id:", paper_id)
        paper = Paper.query.filter_by(id=paper_id).first()
        if mode == 'user' and g.user.id != paper.paper_account_id:
            return jsonify({
                'code': 500,
                'msg': "当前权限错误，不能删除论文"
            })
        if not paper:
            return jsonify({
                'code': 500,
                'msg': "论文不存在，无法删除"
            })
        print("paper:", paper)
        paper_domain = Paper_domain.query.filter_by(paper_id=paper_id).all()
        print("paper_domain:", paper_domain)
        for one in paper_domain:
            db.session.delete(one)
            db.session.commit()
        paper_author = Paper_author.query.filter_by(paper_id=paper_id).all()
        for one in paper_author:
            db.session.delete(one)
            db.session.commit()
        cite = Cite.query.filter_by(citing_paper=paper_id).all()
        for one in cite:
            db.session.delete(one)
            db.session.commit()
        document = Document.query.filter_by(doucument_paper_id=paper_id).first()
        if document:
            db.session.delete(document)
            db.session.commit()
        note = Note.query.filter_by(note_paper_id=paper_id).first()
        if note:
            note.note_paper_id = None
            db.session.commit()
        paper_user = Paper_user.query.filter_by(paper_id=paper_id).first()
        db.session.delete(paper_user)
        db.session.commit()
        db.session.delete(paper)
        db.session.commit()
        return jsonify({
            'code': 200,
            'msg': "删除论文成功"
        })
    except Exception as e:
        print("系统错误")
        return jsonify({
            'code': 500,
            'msg': "删除论文失败"
        })
