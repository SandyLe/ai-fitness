# 配置说明

## 数据库配置

项目使用MySQL数据库存储用户信息、康训数据等。需要在 [app/config.py](file:///d%3A/myItem/%E6%99%BA%E8%83%BD%E5%81%A5%E8%BA%AB%E8%BE%85%E5%8A%A9%E7%B3%BB%E7%BB%9F/AI_Fitness/app/config.py) 文件中配置数据库连接信息：

```python
DB_CONFIG = {
    'host': 'your_database_host',      # 数据库主机地址
    'user': 'your_database_user',      # 数据库用户名
    'password': 'your_database_password',  # 数据库密码
    'database': 'your_database_name'   # 数据库名称
}
```

## AI API配置

项目集成了讯飞星火AI API用于智能助手功能。需要在 [app/config.py](file:///d%3A/myItem/%E6%99%BA%E8%83%BD%E5%81%A5%E8%BA%AB%E8%BE%85%E5%8A%A9%E7%B3%BB%E7%BB%9F/AI_Fitness/app/config.py) 文件中配置API密钥：

```python
AI_API_CONFIG = {
    'appid': 'your_appid',          # 讯飞星火API AppID
    'api_secret': 'your_api_secret',    # 讯飞星火API Secret
    'api_key': 'your_api_key',       # 讯飞星火API Key
    'domain': 'general',            # API领域版本
    'Spark_url': 'wss://spark-api.xf-yun.com/v3.5/chat'  # API接口地址
}
```

## Flask应用配置

Flask应用的密钥在 [app/config.py](file:///d%3A/myItem/%E6%99%BA%E8%83%BD%E5%81%A5%E8%BA%AB%E8%BE%85%E5%8A%A9%E7%B3%BB%E7%BB%9F/AI_Fitness/app/config.py) 中配置：

```python
import uuid
SECRET_KEY = str(uuid.uuid4())  # 用于会话安全的密钥，使用随机生成的字符串
```

## 数据库初始化

项目提供了 [work_out.sql](file:///d%3A/myItem/%E6%99%BA%E8%83%BD%E5%81%A5%E8%BA%AB%E8%BE%85%E5%8A%A9%E7%B3%BB%E7%BB%9F/AI_Fitness/work_out.sql) 文件用于初始化数据库表结构和基础数据。请在MySQL数据库中执行该SQL文件以创建所需的表结构。