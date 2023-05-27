class Config:
    def __init__(self, app):
        # 初始化
        self.configs = {}
        self.app = app

        # 通用详细配置
        # -- 安全性配置
        self.configs['SECRET_KEY'] = 'hard to guess string'
        # -- 数据库连接配置
        self.configs['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
        self.configs['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.configs['SQLALCHEMY_RECORD_QUERIES'] = True
        self.configs['SQLALCHEMY_DATABASE_USERNAME'] = 'jyy'
        self.configs['SQLALCHEMY_DATABASE_PASSWORD'] = 'openGauss_123'
        self.configs['SQLALCHEMY_DATABASE_HOSTNAME'] = '123.60.17.67:8887'
        self.configs['SQLALCHEMY_DATABASE_NAME'] = 'databaseLab'
        self.configs['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + self.configs['SQLALCHEMY_DATABASE_USERNAME'] + ':' \
                                                  + self.configs['SQLALCHEMY_DATABASE_PASSWORD'] + '@' + self.configs[
                                                      'SQLALCHEMY_DATABASE_HOSTNAME'] + '/' \
                                                  + self.configs['SQLALCHEMY_DATABASE_NAME']
        # -- 邮箱配置
        self.configs['MAIL_SUBJECT_PREFIX'] = '【论文管理系统】'
        self.configs['MAIL_SUBJECT_SENDER'] = '3424288785@qq.com'
        self.configs['MAIL_SERVER'] = 'smtp.qq.com'
        self.configs['MAIL_USERNAME'] = '3424288785@qq.com'
        self.configs['MAIL_PASSWORD'] = 'sdpdoidiekcgchjc'
        self.configs['MAIL_USE_TLS'] = True
        self.configs['MAIL_PORT'] = 587

        # 根据config_name来确认具体模式：

        # -- 保存到app对象
        for key in self.configs.keys():
            app.config[key] = self.configs[key]

    def get(self, key):
        if self.configs.__contains__(key):
            return self.configs[key]
