from flask import jsonify, make_response, request, current_app
from flask_httpauth import HTTPBasicAuth
from app import create_app, api

app = create_app()
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(name_or_token, password):
    # 路由拦截白名单设置
    request_path = request.path
    if request_path == '/api/register' or request_path == '/api/getVerifyCode' or request_path == '/api/nameNoRepeat':
        return True
    # 对admin的分发验证
    if request_path[:10:] == '/api/admin':
        return api.verify_password_admin(name_or_token, password)
    # 一般情况
    return api.verify_password_user(name_or_token, password)


@app.before_request
@auth.login_required
def before_request():
    pass


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': '未授权的访问'}), 401)


# 超管页面的api-------------------------------------------
@app.route('/api/adminLogin', methods=['POST'])
def get_auth_token_admin():
    return api.get_auth_token_admin()


@app.route('/api/adminSetpwd', methods=['POST'])
def set_auth_pwd():
    return api.set_auth_pwd_admin()


@app.route('/api/adminGetUserList', methods=['GET'])
def get_user_list():
    return api.get_user_list()


@app.route('/api/adminUserRemove', methods=['GET'])
def remove_user():
    return api.remove_user()


@app.route('/api/adminBatchRemove', methods=['GET'])
def batchremove_user():
    return api.batchremove_user()


@app.route('/api/adminSetUserList', methods=['GET'])
def set_user_permit():
    return api.set_user_permit()

# 与研究方向相关的api--------------------------------------
@app.route('/api/getDomainList', methods=['GET'])
def get_domain_list():
    return api.get_domain_list()


@app.route('/api/adminAddDomainList', methods=['GET'])
def add_domain_list():
    return api.add_domain_list()


@app.route('/api/adiminDeleteDomainList', methods=['GET'])
# post 要改成get吗
def delete_domain():
    return api.delete_domain()


@app.route('/api/adminUpdateDomain', methods=['GET'])
def update_domain():
    return api.update_domain()


@app.route('/api/paperView', methods=['GET'])
def paper_details():
    return api.paper_details()


# 与用户账户相关的api--------------------------------------
@app.route('/api/nameNoRepeat', methods=['POST'])
def nameNoRepeat():
    return api.name_not_in_db()


@app.route('/api/register', methods=['POST'])
def account_register():
    return api.account_register()


@app.route('/api/login', methods=['POST'])
def get_auth_token_user():
    return api.get_auth_token_user()


@app.route('/api/getVerifyCode', methods=['POST'])
def get_verify_code():
    return api.get_verify_code()


# 与论文管理相关的api--------------------------------------


@app.route('/api/myPaperList', methods=['GET'])
def get_mypaper_list():
    return api.get_mypaper_list()


@app.route('/api/getPaperList', methods=['GET'])
def query_papers():
    return api.query_papers()


@app.route('/api/publishPaper', methods=['GET'])
def post_paper():
    return api.post_paper()


@app.route('/api/getPaperListByTitles')
def query_lot_paper_by_titles():
    return api.query_lot_paper_by_titles()


@app.route('/api/updatePaper', methods=['GET'])
def update_paper():
    return api.update_paper()


@app.route('/api/deletePaper', methods=['GET'])
def delete_paper_user():
    return api.delete_paper('user')


@app.route('/api/adminDeletePaper', methods=['GET'])
def delete_paper_admin():
    return api.delete_paper('admin')


@app.route('/api/getMyCommentList', methods=['GET'])
def get_my_comment_list():
    return api.get_comment_list('my')


# 与文件接收相关的api（这个api是通用的）------------------
@app.route('/api/receiveAFile', methods=['POST'])
def receive_a_file():
    from files.receive_file import receive_a_file
    return receive_a_file()


@app.route('/api/getAFile', methods=['GET'])
def get_a_file():
    from files.get_file import get_a_file
    return get_a_file()


# 与笔记相关的api--------------------------------------
@app.route('/api/getNoteList', methods=['GET'])
def get_note_list():
    return api.get_note_list()


@app.route('/api/addNote', methods=['GET'])
def add_note():
    return api.add_note()


@app.route('/api/canIAddNote', methods=['GET'])
def can_i_add_note():
    return api.can_i_add_note()


# 与评论和回复相关的api--------------------------------------
@app.route('/api/getCommentList', methods=['GET'])
def get_comment_list():
    return api.get_comment_list('note')


@app.route('/api/addComment', methods=['GET'])
def add_comment():
    return api.add_comment()


@app.route('/api/addReply', methods=['GET'])
def add_reply():
    return api.add_reply()


@app.route('/api/deleteReply', methods=['GET'])
def delete_reply():
    return api.delete_reply()


@app.route('/api/deleteComment', methods=['GET'])
def delete_comment():
    return api.delete_comment()


@app.route('/api/deleteNote', methods=['GET'])
def deleteNote():
    return api.delete_note()


# 图表展示的api----------------------------------------
@app.route('/api/getDrawPieChart', methods=['GET'])
def get_domain_pic():
    return api.domain_pic('user')


@app.route('/api/adminDrawPieChart', methods=['GET'])
def get_domain_pic_admin():
    return api.domain_pic('admin')


if __name__ == '__main__':
    app.run('0.0.0.0')
