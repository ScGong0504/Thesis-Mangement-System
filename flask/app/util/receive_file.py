import time

from flask import request
from config import file_path


ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF', 'csv'}


def receive_a_file():
    file = request.files['only_one_file']  # Flask中获取文件
    file_name = request.form.get('file_name')
    print('收到文件:', file_name)
    if file is None:
        # 表示没有发送文件
        return {'msg': '转储失败'}, 400
    # 保存文件
    new_file_name = file_path + file_name.rsplit('.', 1)[0] + str(time.time()) + '.' + file_name.rsplit('.', 1)[1]
    file.save(new_file_name)
    return {'msg': '转储成功'}, 200, new_file_name


# 判断文件是否合法
def allowed_file(filename, allowed_extions=None):
    return '.' in filename and filename.rsplit('.', 1)[1] in (allowed_extions or ALLOWED_EXTENSIONS)
