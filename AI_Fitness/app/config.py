# 数据库配置示例
DB_CONFIG = {
    'host': '8.152.98.118',      # 数据库主机地址
    'user': 'root',      # 数据库用户名
    'port': 3309,      # 数据库用户名
    'password': '123456',  # 数据库密码
    'database': 'work_out'   # 数据库名称
}
# DB_CONFIG = {
#     'host': '106.12.15.6',      # 数据库主机地址
#     'user': 'root',      # 数据库用户名
#     'port': '3306',      # 数据库用户名
#     'password': '1qaz@WSX3edc',  # 数据库密码
#     'database': 'work_out'   # 数据库名称
# }

# AI API配置示例
AI_API_CONFIG = {
    'appid': 'your_appid',          # 讯飞星火API AppID
    'api_secret': 'your_api_secret',    # 讯飞星火API Secret
    'api_key': 'your_api_key',       # 讯飞星火API Key
    'domain': 'general',            # API领域版本
    'Spark_url': 'wss://spark-api.xf-yun.com/v3.5/chat'  # API接口地址
}

# Flask应用配置
import uuid
SECRET_KEY = str(uuid.uuid4())  # 用于会话安全的密钥，使用随机生成的字符串