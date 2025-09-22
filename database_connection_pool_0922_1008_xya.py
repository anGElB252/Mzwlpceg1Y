# 代码生成时间: 2025-09-22 10:08:14
import psycopg2
from psycopg2 import pool

# PostgreSQL数据库连接池配置
class DatabaseConnectionPool:
    def __init__(self, minconn, maxconn):
        """
        构造函数，初始化数据库连接池
        :param minconn: 池中最小连接数
        :param maxconn: 池中最大连接数
        """
        self.pool = pool.ThreadedConnectionPool(
            minconn,
            maxconn,
            host="your_host",
            database="your_database",
            user="your_username",
            password="your_password"
        )

    def get_connection(self):
        """
        从连接池中获取一个连接
        :return: 数据库连接
        """
        try:
            conn = self.pool.getconn()
            return conn
        except pool.PoolError as e:
            print(f"Error retrieving connection from pool: {e}")
            return None

    def release_connection(self, conn):
        """
        将连接放回连接池
        :param conn: 放回的数据库连接
        """
        try:
            self.pool.putconn(conn)
        except Exception as e:
            print(f"Error releasing connection to pool: {e}")

    def close_all_connections(self):
        """
        关闭连接池中的所有连接
        """
        self.pool.closeall()

# 使用示例
if __name__ == "__main__":
    # 创建连接池实例，设置最小1个连接，最大10个连接
    pool = DatabaseConnectionPool(minconn=1, maxconn=10)

    # 获取数据库连接
    conn = pool.get_connection()
    if conn:
        # 使用连接进行数据库操作
        # 示例：创建游标并执行SQL查询
        cur = conn.cursor()
        cur.execute("SELECT * FROM your_table")
        records = cur.fetchall()
        print(records)
        # 释放连接
        pool.release_connection(conn)

    # 关闭所有连接
    pool.close_all_connections()
