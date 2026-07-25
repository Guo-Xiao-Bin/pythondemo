import pymysql

from common.recordlog import logs
from conf.operationConfig import OperationConfig

conf = OperationConfig()


class ConnectMysql:
    """连接读取MySQL数据库的数据"""

    def __init__(self):
        mysql_conf = {
            'host': conf.get_mysql_conf('host'),
            'port': int(conf.get_mysql_conf('port')),
            'user': conf.get_mysql_conf('username'),
            'password': conf.get_mysql_conf('password'),
            'database': conf.get_mysql_conf('database'),
        }
        try:
            # 连接mysql数据库
            self.conn = pymysql.connect(**mysql_conf, charset='utf8')
            # 游标，cursor=pymysql.cursors.DictCursor将数据库表字段显示，以key-value形式显示
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            logs.info("""成功连接到MySQL数据库
            host:{host}
            port:{port}
            db:{database}""".format(**mysql_conf))
        except Exception as e:
            logs.error(e)

    def close(self):
        if self.conn and self.cursor:
            self.cursor.close()
            self.conn.close()

    def query(self, sql):
        """查询数据"""
        try:
            # 将sql语句传给mysql服务器执行，只执行不提交，执行的数据只停留在缓冲区中
            self.cursor.execute(sql)
            # 提交事物，把缓冲区的修改永久写入数据库（查询不需要提交）
            self.conn.commit()
            # 获取mysql返回的结果
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            logs.error(e)
        # 无论走上面哪条路都会走finally
        finally:
            # 关闭连接
            self.close()

    def insert(self, sql):
        """新增"""
        pass

    def update(self, sql):
        """修改"""
        pass

    def delete(self, sql):
        """删除"""
        pass


if __name__ == '__main__':
    conn = ConnectMysql()
    sql = 'select * from ecs_goods limit 5'
    print(conn.query(sql))
