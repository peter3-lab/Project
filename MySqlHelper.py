import pymysql

class MySqlHelper:
    """
    一个用于简化MySQL数据库操作的帮助类。
    使用 with 语句可以自动管理连接的打开和关闭。
    """
    def __init__(self, host, port, user, password, database):
        """
        初始化数据库连接信息。
        """
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor  # 使查询结果以字典形式返回
        }
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """
        当进入 with 语句块时，建立数据库连接。
        """
        self.connection = pymysql.connect(**self.config)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        当退出 with 语句块时，关闭游标和连接。
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, sql, params=None):
        """
        执行查询类操作 (SELECT)。
        :param sql: SQL查询语句
        :param params: SQL语句的参数，用于防止SQL注入
        :return: 查询结果列表
        """
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def execute_update(self, sql, params=None):
        """
        执行更新类操作 (INSERT, UPDATE, DELETE)。
        :param sql: SQL执行语句
        :param params: SQL语句的参数
        :return: 受影响的行数
        """
        try:
            affected_rows = self.cursor.execute(sql, params)
            self.connection.commit()
            return affected_rows
        except Exception as e:
            self.connection.rollback()
            print(f"执行失败: {e}")
            return 0

# --- 使用示例 ---
if __name__ == '__main__':
    # 你的数据库连接信息
    db_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root', # 替换为你的用户名
        'password': '123456', # 替换为你的密码
        'database': 'project_db'
    }

    try:
        with MySqlHelper(**db_config) as db:
            # 示例：插入数据
            sql_insert = "INSERT INTO students (name, height) VALUES (%s, %s)"
            db.execute_update(sql_insert, ('赵六', 190.00))
            print("插入数据成功。")

            # 示例：查询数据
            sql_select = "SELECT * FROM students"
            results = db.execute_query(sql_select)
            print("当前所有学生:")
            for row in results:
                print(row)

    except pymysql.err.OperationalError as e:
        print(f"无法连接到数据库，请检查配置或数据库服务是否已启动: {e}")