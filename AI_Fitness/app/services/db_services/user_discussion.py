#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fitenss_items
@File    ：user_discussion.py
@IDE     ：PyCharm
@Author  ：写BUG的Botter
@Date    ：2025/4/11 08:51
'''
from datetime import datetime

"""用户论坛模块"""

from app.config import DB_CONFIG
from app.utils.libmysql import MYSQL
from app.utils.result_type import Response
conn = MYSQL(
        dbhost = DB_CONFIG['host'],
        dbuser = DB_CONFIG['user'],
        dbpwd = DB_CONFIG['password'],
        dbname = DB_CONFIG['database'],
        dbcharset = 'utf8')

TABLE_NAME = "user_discussion"

"""添加论坛信息"""
def add_discussion(discussion_data: dict):
    # 基础校验
    if not discussion_data or len(discussion_data) == 0:
        return Response.fail(code=500, msg="提交信息为空")

    # 必填字段校验 (根据 DDL 和常识，title 和 content 通常是必须的)
    required_fields = ['title', 'content']
    for field in required_fields:
        if field not in discussion_data or not discussion_data.get(field):
            return Response.fail(code=500, msg=f"字段 {field} 不能为空")

    # 准备插入的数据
    insert_data = discussion_data.copy()
    now = datetime.now()
    insert_data['created_time'] = now
    insert_data['update_time'] = now # ddl uses update_time
    insert_data.setdefault('is_deleted', 0)
    # created_by and update_by should ideally be set based on logged-in user context

    try:
        result_id = conn.insert(TABLE_NAME, insert_data)
        return Response.success(data={"id": result_id})
    except Exception as e:
        return Response.fail(code=500, msg=f"论坛信息创建失败: {str(e)}")
discussion_data = {'title': 'Test Title', 'content': 'Test content', 'created_by': 1}
# print(add_discussion(discussion_data))
"""修改论坛信息"""
def update_discussion(discussion_id: int, update_data: dict):
    """根据ID修改论坛信息"""
    if not discussion_id:
        return Response.fail(code=500, msg="论坛ID不能为空")
    if not update_data or len(update_data) == 0:
        return Response.fail(code=500, msg="更新信息为空")

    # 不允许修改主键
    if 'id' in update_data:
        del update_data['id']

    # 补充更新时间
    update_data['update_time'] = datetime.now()
    # update_by should be set based on context

    condition = {"id": discussion_id, "is_deleted": 0} # 只能更新未删除的

    try:
        affected_rows = conn.update(TABLE_NAME, update_data, condition=condition)
        if affected_rows > 0:
            return Response.success(msg="论坛信息更新成功")
        else:
            return Response.fail(code=404, msg="未找到论坛信息或无需更新")
    except Exception as e:
        return Response.fail(code=500, msg=f"论坛信息更新失败: {str(e)}")

"""删除论坛信息"""
def delete_discussion_by_id(discussion_id: int):
    """根据ID删除论坛信息 (逻辑删除)"""
    if not discussion_id:
        return Response.fail(code=500, msg="论坛ID不能为空")

    update_data = {
        "is_deleted": 1,
        "update_time": datetime.now()
        # update_by should be set based on context
    }
    condition = {"id": discussion_id}

    try:
        affected_rows = conn.update(TABLE_NAME, update_data, condition=condition)
        if affected_rows > 0:
            return Response.success(msg="论坛信息删除成功")
        else:
            return Response.fail(code=404, msg="未找到要删除的论坛信息或无需更新")
    except Exception as e:
        return Response.fail(code=500, msg=f"论坛信息删除失败: {str(e)}")

"""查询论坛信息"""
def get_discussion(condition: dict):
    """获取论坛信息，允许传入查询条件字典，默认只查询未删除的"""
    if not condition or len(condition) == 0:
        return Response.fail(code=500, msg="查询条件不能为空")

    # 默认查询未删除的
    condition.setdefault('is_deleted', 0)

    try:
        result = conn.fetch_rows(TABLE_NAME, condition=condition)
        if result is None or len(result) == 0:
            return Response.fail(code=404, msg="查无此论坛信息")
        # 如果是根据唯一ID查询，通常只返回一条记录
        if "id" in condition and len(result) == 1:
             return Response.success(data=result[0]) # 返回单个对象而非列表
        return Response.success(data=result) # 返回列表
    except Exception as e:
        return Response.fail(code=500, msg=f"查询论坛信息失败: {str(e)}")

def get_discussion_by_id(discussion_id: int):
     """根据ID获取单个论坛信息"""
     if not discussion_id:
         return Response.fail(code=500, msg="论坛ID不能为空")
     return get_discussion({"id": discussion_id})

def count_discussions(condition: dict = None):
    """根据条件统计论坛数量，默认统计未删除的"""
    query_condition = condition.copy() if condition else {}
    query_condition.setdefault('is_deleted', 0)
    try:
        count = conn.count(table=TABLE_NAME, condition=query_condition)
        return Response.success(data=count)
    except Exception as e:
        return Response.fail(code=500, msg=f"统计论坛信息失败: {str(e)}")

# print(add_discussion({
#         "title":"如何健身",
#         "content":"1.坚持打卡 ， 2.坚持锻炼",
#         "image_path" : "https://123.png",
#         "created_by" : None ,
#         "created_time" : datetime.now(),
#         "update_by": None ,
#         "update_time":datetime.now(),
#         }))





# print(update_discussion({
#         "id": 22,
#         "title":"如何健身",
#         "content":"1.坚持打卡",
#         "image_path" : "https://123.png",
#         "created_by" : None ,
#         "created_time" : datetime.now(),
#         "update_by": None ,
#         "update_time":datetime.now(),
# },
#     {
#         "id": 22,
#         "title": "如何健身",
#         "content": "1.坚持打卡 ， 2.坚持锻炼",
#         "image_path": "https://123.png",
#         "created_by": None,
#         "created_time": datetime.now(),
#         "update_by": None,
#         "update_time": datetime.now(),
#     }
# ))