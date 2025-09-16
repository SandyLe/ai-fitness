#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fitenss_items
@File    ：user_info.py
@IDE     ：PyCharm
@Author  ：写BUG的Botter
@Date    ：2025/4/11 08:51
'''
import re
from datetime import datetime

from app.config import DB_CONFIG
from app.utils.libmysql import MYSQL
from app.utils.result_type import Response

conn = MYSQL(
    dbhost=DB_CONFIG['host'],
    dbuser=DB_CONFIG['user'],
    dbpwd=DB_CONFIG['password'],
    dbname=DB_CONFIG['database'],
    dbcharset='utf8'
)

TABLE_NAME = "user_info"


def add_user(user: dict):
    """增加用户"""
    # 基础校验
    if not user or len(user) == 0:
        return Response.fail(code=500, msg="提交信息为空")

    # 必填字段校验 (根据 DDL 和常识)
    required_fields = ['user_name', 'password', 'email']
    for field in required_fields:
        if field not in user or not user.get(field):
            return Response.fail(code=500, msg=f"字段 {field} 不能为空")

    # 用户名重复校验
    if get_count_username(user['user_name']) > 0:
        return Response.fail(code=500, msg="用户名已存在！")

    # 可选：邮箱格式校验 (如果提供了邮箱)
    if 'email' in user and user['email']:
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_pattern, user['email']):
            return Response.fail(code=400, msg="邮箱格式不合法")

    # 准备插入的数据
    insert_data = user.copy()
    insert_data['created_time'] = datetime.now()
    insert_data['updated_time'] = datetime.now()
    # 可以设置默认值，如 status=1, is_deleted=0 等
    insert_data.setdefault('status', 1)
    insert_data.setdefault('is_deleted', 0)

    try:
        result_id = conn.insert(TABLE_NAME, insert_data)
        return Response.success(data={"id": result_id})
    except Exception as e:
        # 可以记录更详细的日志 e
        return Response.fail(code=500, msg=f"用户创建失败: {str(e)}")


def get_count_username(username):
    """根据用户名查询用户存在数量"""
    if not username:
        return 0
    else:
        cond = {"user_name": username, "is_deleted": 0} # 仅查询未删除的用户
        return conn.count(table=TABLE_NAME, condition=cond)


def delete_user_by_id(user_id: int):
    """根据ID删除用户 (逻辑删除)"""
    if not user_id:
        return Response.fail(code=500, msg="用户ID不能为空")

    update_data = {
        "is_deleted": 1,
        "updated_time": datetime.now()
    }
    condition = {"id": user_id}

    try:
        affected_rows = conn.update(TABLE_NAME, update_data, condition=condition)
        if affected_rows > 0:
            return Response.success(msg="用户删除成功")
        else:
            return Response.fail(code=404, msg="未找到要删除的用户或无需更新")
    except Exception as e:
        return Response.fail(code=500, msg=f"用户删除失败: {str(e)}")

# 可以选择物理删除
# def delete_user_physically_by_id(user_id: int):
#     """根据ID物理删除用户"""
#     if not user_id:
#         return Response.fail(code=500, msg="用户ID不能为空")
#     condition = {"id": user_id}
#     try:
#         affected_rows = conn.delete(TABLE_NAME, condition=condition)
#         if affected_rows > 0:
#             return Response.success(msg="用户物理删除成功")
#         else:
#             return Response.fail(code=404, msg="未找到要删除的用户")
#     except Exception as e:
#         return Response.fail(code=500, msg=f"用户物理删除失败: {str(e)}")


def update_user(user_id: int, update_data: dict):
    """根据ID修改用户信息"""
    if not user_id:
        return Response.fail(code=500, msg="用户ID不能为空")
    if not update_data or len(update_data) == 0:
        return Response.fail(code=500, msg="更新信息为空")

    # 不允许直接修改用户名或主键等敏感/关键信息，如有需要应提供专门接口
    if 'user_name' in update_data:
        del update_data['user_name']
    if 'id' in update_data:
        del update_data['id']

    # 补充更新时间
    update_data['updated_time'] = datetime.now()
    condition = {"id": user_id, "is_deleted": 0} # 只能更新未删除的用户

    try:
        affected_rows = conn.update(TABLE_NAME, update_data, condition=condition)
        if affected_rows > 0:
            return Response.success(msg="用户信息更新成功")
            # 如果需要返回更新后的数据，可以再查询一次
            # updated_user = get_user({"id": user_id})
            # return updated_user
        else:
            # 可能是用户不存在，或者提交的数据与原数据相同
            return Response.fail(code=404, msg="未找到用户或无需更新")
    except Exception as e:
        return Response.fail(code=500, msg=f"用户信息更新失败: {str(e)}")


def get_user(condition: dict):
    """
    获取用户信息，允许传入查询条件字典
    例如: get_user({"id": 1}) 或 get_user({"user_name": "Botter"})
    默认只查询未删除的用户
    """
    if not condition or len(condition) == 0:
        return Response.fail(code=500, msg="查询条件不能为空")

    try:
        result = conn.fetch_rows(TABLE_NAME, condition=condition)
        if result is None or len(result) == 0:
            return Response.fail(code=404, msg="查无此用户")
        # 如果是根据唯一ID查询，通常只返回一条记录
        if "id" in condition and len(result) == 1:
             return Response.success(data=result[0]) # 返回单个对象而非列表
        return Response.success(data=result) # 返回列表
    except Exception as e:
        return Response.fail(code=500, msg=f"查询用户失败: {str(e)}")


def get_user_by_id(user_id: int):
     """根据ID获取单个用户信息"""
     if not user_id:
         return Response.fail(code=500, msg="用户ID不能为空")
     return get_user({"id": user_id})

# user = {
#     "user_name":"Test",
#     "email":"3333@xxx.com",
#     "password":"123456"
# }
# print(add_user(user))
# print(add_user(None))
#
# print(get_user_info({"user_name":"Botter"}))
# print(get_user_info({"id": 1}))
# user = {
#     "user_name":"zzz",
#     "password":"23456"
# }
# print(update_user(user))

# print(get_count_username("Botter"))



# print(verify_user({
#     "user_name": "zzz",
#     "password": "123456"
# }))