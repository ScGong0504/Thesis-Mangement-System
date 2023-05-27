from flask import request, send_file, jsonify, make_response
import os

file_path = os.getcwd() + os.sep + 'files' + os.sep + 'files' + os.sep


def get_a_file():
    file_name = request.args.get('file_name')
    # 只有安全·文件夹中的文件才能被发送
    print(file_name)
    if file_name is None:
        print('错误！该文件不存在')
        return make_response(jsonify({'msg': '该文件不存在'}), 400)
    elif file_name[:file_name.rindex(os.sep) + 1:] == file_path:
        return send_file(file_name)
    else:
        print('错误！该文件不可访问')
        return make_response(jsonify({'msg': '该文件不可访问'}), 400)
