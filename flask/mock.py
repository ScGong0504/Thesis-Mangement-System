from app import create_app
from app.models import User

app = create_app()
app.app_context().push()

# User.add('yz', '123456', 'email')
# Admin.add('yz')
#
# for i in range(0, 10):
#     User.add('yz' + str(i), '123456', str(i) + '@qq.com')
#     print('User:' + 'yz' + str(i) + '已创建')

user = User.query.get(1)
user.improve_permit()

