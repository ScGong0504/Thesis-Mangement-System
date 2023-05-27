from datetime import datetime

from app import db
from flask import g
from manage import app
from sqlalchemy import or_

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from passlib.apps import custom_app_context


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True)
    password = db.Column(db.Text)
    phone = db.Column(db.String(30))
    process = db.Column(db.String(30))
    role = db.Column(db.Integer)  # 1普通管理员 0用户
    address = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True)
    info = db.Column(db.Text)
    register_date = db.Column(db.DateTime, default=datetime.now())

    def to_dict(self):
        columns = self.__table__.columns.keys()
        result = {}
        for key in columns:
            if key == 'register_date' or key == 'password':
                value = getattr(self, key).strftime("%Y-%m-%d %H:%M:%S")
            else:
                value = getattr(self, key)
            result[key] = value
        return result

    def to_dict1(self):
        columns = self.__table__.columns.keys()
        result = {}
        for key in columns:
            if key == 'id' or key == 'name' or key == 'phone' or key == 'email' or key == 'role':
                value = getattr(self, key)
            else:
                continue
            result[key] = value
        return result

    def improve_permit(self):
        self.role = 1
        admin = Admin.add(self.name)
        db.session.add_all([admin, self])
        db.session.commit()

    def lower_permit(self):
        self.role = 0
        admin = Admin.query.filter_by(name=self.name).first()
        db.session.add(self)
        db.session.delete(admin)
        db.session.commit()

    @staticmethod
    # 密码加密
    def hash_password(self, password):
        self.password = custom_app_context.encrypt(password)

    # 密码解析
    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)

    # 获取token，有效时间10min
    def generate_auth_token(self, expiration=6000):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    # 解析token，确认登录的用户身份
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

    @staticmethod
    def add(username, password, email):
        try:
            user = User(name=username,
                        password=custom_app_context.encrypt(password),
                        email=email,
                        role=0)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print('Error:', e)
            return None
        else:
            return user

    def set_user(self, data):
        self.name = data['username']
        self.phone = data['phone']
        self.address = data['phone']
        self.info = data['info']


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), index=True)

    # 密码验证
    def verify_password(self, password):
        user = User.query.filter_by(name=self.name).first()
        return user.verify_password(password)

    # 获取token，有效时间10min
    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    # 解析token，确认登录的用户身份
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        admin = Admin.query.get(data['id'])
        return admin

    @staticmethod
    def add(username):
        try:
            total = Admin.query.count()
            admin = Admin(id=total+1,name=username)
            db.session.add(admin)
            db.session.commit()
        except Exception as e:
            print('Error:', e)
            return None
        else:
            return admin


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    company = db.Column(db.String(64))

    @staticmethod
    def add(name, email, company):
        try:
            author = Author(name=name, email=email, company=company)
            db.session.add(author)
            db.session.commit()
        except Exception as e:
            print('Error:', e)
            return None
        else:
            return author


class Meeting(db.Model):
    __tablename__ = 'meeting'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meeting_title = db.Column(db.String(64))
    meeting_date = db.Column(db.DateTime, default=datetime.now())
    meeting_detail = db.Column(db.Text)

    @staticmethod
    def add(meeting_title, meeting_date, meeting_detail):
        try:
            meeting = Meeting(meeting_title=meeting_title, meeting_date=meeting_date, meeting_detail=meeting_detail, )
            db.session.add(meeting)
            db.session.commit()
        except Exception as e:
            print('Error:', e)
            return None
        else:
            return meeting


class Domain(db.Model):
    __tablename__ = 'domain'
    domain_name = db.Column(db.String(64), primary_key=True)
    is_deleted = db.Column(db.Integer)

    @staticmethod
    def add(domain_name):
        try:
            domain = Domain(domain_name=domain_name, is_deleted=0)
            db.session.add(domain)
            db.session.commit()
        except Exception as e:
            print('Error:', e)
            return None
        else:
            return domain


class Paper(db.Model):
    __tablename__ = 'paper'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64))
    publish_time = db.Column(db.DateTime, default=datetime.now())
    abstract = db.Column(db.Text)
    type = db.Column(db.Integer)
    issue_date = db.Column(db.DateTime, default=datetime.now())
    body_url = db.Column(db.String(255))
    paper_account_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    paper_meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'))

    @staticmethod
    def add(title, publish_time, abstract, type, issue_date, body_url, paper_account_id, paper_meeting_id):
        try:
            paper = Paper(
                title=title,
                publish_time=publish_time,
                abstract=abstract,
                type=type,
                issue_date=issue_date,
                body_url=body_url,
                paper_account_id=paper_account_id,
                paper_meeting_id=paper_meeting_id
            )
            db.session.add(paper)
            db.session.commit()
        except Exception as e:
            print('Error:', e)
            return None
        else:
            return paper

    def to_dict(self):
        columns = self.__table__.columns.keys()
        result = {}
        for key in columns:
            if key == 'issue_date' or key == 'publish_time' or key == 'abstract':
                # value = getattr(self, key).strftime("%Y-%m-%d %H:%M:%S")
                continue
            elif key == 'type':
                if getattr(self, key) is None:
                    value = ''
                else:
                    value_ = ['理论证明型', '综述型', '实验型', '工具型', '数据集论文型']
                    value = value_[getattr(self, key) - 1]
            elif key == 'paper_account_id':
                user = User.query.get(getattr(self, key))
                value = user.name
                key = 'user'
            elif key == 'paper_meeting_id':
                metting = Meeting.query.get(getattr(self, key))
                value = metting.meeting_title
                key = 'meeting'
            else:
                value = getattr(self, key)
            result[key] = value
        result['domains'] = self.get_domains()
        result['authors'] = self.get_authors()
        return result

    def get_domains(self):
        domains = PaperDomain.query.filter_by(paper_id=self.id).all()
        result = ''
        for d in domains:
            result += d.domain_name + ' '
        return result.strip()

    def get_authors(self):
        author_paper = PaperAuthor.query.filter_by(paper_id=self.id).order_by('level').all()
        result = ''
        for ap in author_paper:
            if Author.query.get(ap.author_id).name is None:
                continue
            result += Author.query.get(ap.author_id).name + ' '
        return result.strip()

    def remove(self):
        db.session.delete(self)
        db.session.commit(self)


class Document(db.Model):
    __tablename__ = 'document'
    document_url = db.Column(db.String(255), primary_key=True)
    document_name = db.Column(db.String(32))
    doucument_paper_id = db.Column(db.Integer, db.ForeignKey('paper.id'))

    @staticmethod
    def add(document_url, document_name, doucument_paper_id):
        try:
            document = Paper(document_url=document_url,
                             document_name=document_name,
                             doucument_paper_id=doucument_paper_id
                             )
            db.session.add(document)
            db.session.commit()
        except Exception as e:
            print('Error:', e)
            return None
        else:
            return document


class Note(db.Model):
    __tablename__ = 'note'
    note_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_content = db.Column(db.Text)
    note_title = db.Column(db.Text)
    note_paper_id = db.Column(db.Integer, db.ForeignKey('paper.id'))

    @staticmethod
    def add(note_content, note_paper_id, note_title):
        try:
            note = Note(note_content=note_content, note_paper_id=note_paper_id, note_title=note_title)
            db.session.add(note)
            db.session.commit()
        except Exception as e:
            print('Error:', e)
            return None
        else:
            return note

    def to_dict(self):
        columns = self.__table__.columns.keys()
        result = {}
        for key in columns:
            value = getattr(self, key)
            result[key] = value
        return result

    def remove(self):
        self.note_content = '该笔记已删除'
        db.session.add(self)
        db.session.commit()


class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment_content = db.Column(db.Text)
    comment_time = db.Column(db.DateTime, default=datetime.now())
    comment_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_note_id = db.Column(db.Integer, db.ForeignKey('note.note_id'))

    @staticmethod
    def add(comment_content, comment_user_id, comment_note_id):
        try:
            comment = Comment(
                comment_content=comment_content,
                comment_user_id=comment_user_id,
                comment_note_id=comment_note_id
            )
            db.session.add(comment)
            db.session.commit()
        except Exception as e:
            print('Error:', e)
            return None
        else:
            return comment

    def to_dict(self):
        columns = self.__table__.columns.keys()
        result = {}
        for key in columns:
            if key == 'comment_time':
                value = getattr(self, key).strftime("%Y-%m-%d %H:%M:%S")
            elif key == 'comment_user_id':
                user = User.query.get(self.comment_user_id)
                value = user.name
                key = 'comment_username'
                result['del_ok'] = user.id == g.user.id
            elif key == 'comment_note_id':
                continue
            else:
                value = getattr(self, key)
            result[key] = value
        result['replys'] = Reply.get_replys(self.comment_id)
        return result

    def remove(self):
        self.comment_content = '该评论已删除'
        db.session.add(self)
        db.session.commit()


class Reply(db.Model):
    __tablename__ = 'reply'
    reply_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reply_content = db.Column(db.Text)
    reply_time = db.Column(db.DateTime, default=datetime.now())
    reply_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reply_comment_id = db.Column(db.Integer, db.ForeignKey('comment.comment_id'))

    @staticmethod
    def help1(reply_id):
        rp = PairReply.query.get(reply_id)
        if rp is None:
            return ''
        else:
            return User.query.get(Reply.query.get(rp.reply2).reply_user_id).name

    @staticmethod
    def get_replys(comment_id):
        replys = Reply.query.filter_by(reply_comment_id=comment_id).all()
        return [{
            'reply_id': r.reply_id,
            'reply_content': r.reply_content,
            'reply_time': r.reply_time.strftime("%Y-%m-%d %H:%M:%S"),
            'username1': Reply.help1(r.reply_id),  # 被回复的
            'username2': User.query.get(r.reply_user_id).name,  # 回复的
            'del_ok': r.reply_user_id == g.user.id
        } for r in replys]

    @staticmethod
    def add(reply_content, reply_user_id, reply_comment_id):
        try:
            reply = Reply(
                reply_content=reply_content,
                reply_user_id=reply_user_id,
                reply_comment_id=reply_comment_id
            )
            db.session.add(reply)
            db.session.commit()
        except Exception as e:
            print('Error:', e)
            return None
        else:
            return reply

    def remove(self):
        self.reply_content = '该回复已删除'
        db.session.add(self)
        db.session.commit()


class PaperUser(db.Model):
    __tablename__ = 'paper_user'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('paper.id'), primary_key=True)

    @staticmethod
    def add(user_id, paper_id):
        try:
            paper_user = PaperUser(user_id=user_id, paper_id=paper_id)
            db.session.add(paper_user)
            db.session.commit()
        except Exception as e:
            print('Error:', e)
            return None
        else:
            return paper_user


class ExtendDomain(db.Model):
    __tablename__ = 'extend_domain'
    parent_domain = db.Column(db.String(64), db.ForeignKey('domain.domain_name'), primary_key=True)
    child_domain = db.Column(db.String(64), db.ForeignKey('domain.domain_name'), primary_key=True)

    @staticmethod
    def add(parent_domain, child_domain):
        try:
            parent_domain = ExtendDomain(parent_domain=parent_domain, child_domain=child_domain)
            db.session.add(parent_domain)
            db.session.commit()
        except Exception as e:
            print('Error:', e)
            return None
        else:
            return parent_domain


class PaperDomain(db.Model):
    __tablename__ = 'paper_domain'
    paper_id = db.Column(db.Integer, db.ForeignKey('paper.id'), primary_key=True)
    domain_name = db.Column(db.String(64), db.ForeignKey('domain.domain_name', primary_key=True))

    @staticmethod
    def add(paper_id, domain_name):
        try:
            paperdomain = PaperDomain(paper_id=paper_id, domain_name=domain_name)
            db.session.add(paperdomain)
            db.session.commit()
        except Exception as e:
            print('Error:', e)
            return None
        else:
            return paperdomain


class PaperAuthor(db.Model):
    __tablename__ = 'paper_author'
    paper_id = db.Column(db.Integer, db.ForeignKey('paper.id'), primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), primary_key=True)
    level = db.Column(db.Integer)

    @staticmethod
    def add(paper_id, author_id, level):
        try:
            paper_author = PaperAuthor(paper_id=paper_id, author_id=author_id, level=level)
            db.session.add(paper_author)
            db.session.commit()
        except Exception as e:
            print('Error:', e)
            return None
        else:
            return paper_author


class PairReply(db.Model):
    __tablename__ = 'pair_reply'
    reply1 = db.Column(db.Integer, db.ForeignKey('reply.reply_id'), primary_key=True)
    reply2 = db.Column(db.Integer, db.ForeignKey('reply.reply_id'))

    @staticmethod
    def add(reply1, reply2):
        try:
            pr = PairReply(reply1=reply1, reply2=reply2)
            db.session.add(pr)
            db.session.commit()
        except Exception as e:
            print('Error:', e)
            return None
        else:
            return pr

    def remove(self):
        db.session.delete(self)
        db.session.commit()


class Cite(db.Model):
    __tablename__ = 'cite'
    citing_paper = db.Column(db.Integer, db.ForeignKey('paper.id'), primary_key=True)
    cited_paper = db.Column(db.Integer, db.ForeignKey('paper.id'), primary_key=True)

    @staticmethod
    def add(citing_paper, cited_paper):
        try:
            cite = Cite(citing_paper=citing_paper, cited_paper=cited_paper)
            db.session.add(cite)
            db.session.commit()
        except Exception as e:
            print('Error:', e)
            return None
        else:
            return cite
