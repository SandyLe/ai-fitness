from dbutils.pooled_db import PooledDB
import pymysql
import threading
from typing import List, Dict, Any, Tuple
from pymysql.cursors import DictCursor

class ConnectionPool:
    """数据库连接池"""
    _instance = None
    _lock = threading.Lock()
    def __new__(cls, config: Dict[str, Any]):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.pool_config = config.copy()
                cls._instance._pool = PooledDB(
                    creator=pymysql,
                    maxconnections=20, # 最大连接数
                    mincached=2, # 初始空闲连接
                    maxcached=10, # 最大空闲连接
                    blocking=True, # 连接耗尽时等待
                    ping=1, # 使用时检查连接
                    **config
                )
        return cls._instance

    def get_connection(self):
        """从连接池获取连接"""
        return self._pool.connection()

# 使用连接池的数据库管理器
class PooledDBManager:
    def __init__(self, pool_config: Dict[str, Any]):
        self.pool = ConnectionPool(pool_config)
    def execute_query(self, sql: str, params: Tuple = None) -> List[Dict]:
        """执行查询"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor(DictCursor) as cursor:
                cursor.execute(sql, params or ())
                return cursor.fetchall()
        finally:
            conn.close() # 实际是放回连接池

    def execute_update(self, sql: str, params: Tuple = None) ->int:
        """执行更新"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                affected_rows = cursor.execute(sql, params or ())
                conn.commit()
                return affected_rows
        except Exception as e:
            conn.rollback()
            raise e
        finally:
           conn.close()