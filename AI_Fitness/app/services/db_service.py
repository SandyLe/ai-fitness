import pymysql
from app.config import DB_CONFIG

def get_connection():
    """获取数据库连接"""
    return pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        port=DB_CONFIG['port']
    )

# 在db_service.py中添加以下函数

def verify_user(username, password):
    """验证用户登录信息"""
    # 实现用户验证逻辑
    # 返回用户信息或None

def user_exists(username):
    """检查用户名是否已存在"""
    # 实现检查逻辑
    # 返回布尔值

def create_user(username, password):
    """创建新用户"""
    # 实现用户创建逻辑
    # 返回新用户ID

def search_user_datas(user_id):
    """查询用户数据"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        sql = "SELECT * FROM user WHERE id = %s"
        cursor.execute(sql, (user_id,))
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"查询用户数据出错: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def idlst():
    """获取所有用户ID列表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        sql = "SELECT id FROM user"
        cursor.execute(sql)
        results = cursor.fetchall()
        return [result[0] for result in results]
    except Exception as e:
        print(f"获取用户ID列表出错: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def add_datas(name, id, password):
    """添加用户数据"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        sql = "INSERT INTO user (name, id, password) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, id, password))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"添加用户数据出错: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def updatedaka(user_id, current_time, day):
    """更新打卡信息"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        sql = "UPDATE user SET day = %s, ontime = %s WHERE id = %s"
        cursor.execute(sql, (day, current_time, user_id))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"更新打卡信息出错: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def search_luntan_datas():
    """查询论坛数据"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        sql = "SELECT * FROM luntan"
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"查询论坛数据出错: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def add_luntan_datas(user_id, image_path, title, content):
    """添加论坛数据"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 获取用户信息
        user_sql = "SELECT name FROM user WHERE id = %s"
        cursor.execute(user_sql, (user_id,))
        user_name = cursor.fetchone()[0]
        
        # 插入论坛数据
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        sql = "INSERT INTO luntan (author, image, title, content, time) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (user_name, image_path, title, content, current_time))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"添加论坛数据出错: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delect_luntan_datas(user_id, post_id, post_author, post_content, post_time):
    """删除论坛数据"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        sql = "DELETE FROM luntan WHERE id = %s AND author = %s AND content = %s AND time = %s"
        cursor.execute(sql, (post_id, post_author, post_content, post_time))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"删除论坛数据出错: {e}")
        return False
    finally:
        cursor.close()
        conn.close()