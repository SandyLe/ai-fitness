#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fitenss_items
@File    ：user_topic.py
@IDE     ：PyCharm
@Author  ：写BUG的Botter
@Date    ：2025/4/12
'''
from datetime import datetime

from app.config import DB_CONFIG
from app.utils.libmysql import MYSQL
from app.utils.result_type import Response

conn = MYSQL(
    dbhost=DB_CONFIG['host'],
    dbuser=DB_CONFIG['user'],
    dbpwd=DB_CONFIG['password'],
    dbname=DB_CONFIG['database'],
    dbport=DB_CONFIG['port'],
    dbcharset='utf8'
)

TABLE_NAME = "user_topic"


def add_topic(topic_data: dict):
    """增加论坛回复 (主题帖)"""
    if not topic_data or len(topic_data) == 0:
        return Response.fail(code=500, msg="提交信息为空")

    # 必填字段校验
    required_fields = ['discussion_id'] # parent_id can be null for top-level
    for field in required_fields:
        if field not in topic_data or topic_data.get(field) is None:
             return Response.fail(code=500, msg=f"字段 {field} 不能为空")

    # 准备插入的数据
    insert_data = topic_data.copy()
    now = datetime.now()
    insert_data['created_time'] = now
    insert_data['update_time'] = now
    # created_by and update_by should ideally be set based on logged-in user context

    try:
        result_id = conn.insert(TABLE_NAME, insert_data)
        return Response.success(data={"id": result_id})
    except Exception as e:
        return Response.fail(code=500, msg=f"创建回复失败: {str(e)}")


def update_topic(topic_id: int, update_data: dict):
    """根据ID修改回复信息 (e.g., audit fields, content if added)"""
    if not topic_id:
        return Response.fail(code=500, msg="回复ID不能为空")
    if not update_data or len(update_data) == 0:
        return Response.fail(code=500, msg="更新信息为空")

    # 不允许修改主键或外键
    for forbidden_key in ['id', 'parent_id', 'discussion_id']:
         if forbidden_key in update_data:
             del update_data[forbidden_key]

    if not update_data:
        return Response.fail(code=400, msg="没有可更新的字段")

    # 补充更新时间
    update_data['update_time'] = datetime.now()
    # update_by should be set based on context

    condition = {"id": topic_id} # No is_deleted check

    try:
        affected_rows = conn.update(TABLE_NAME, update_data, condition=condition)
        if affected_rows > 0:
            return Response.success(msg="回复信息更新成功")
        else:
            return Response.fail(code=404, msg="未找到回复信息或无需更新")
    except Exception as e:
        return Response.fail(code=500, msg=f"回复信息更新失败: {str(e)}")


def delete_topic_by_id(topic_id: int):
    """根据ID删除回复 (物理删除)"""
    if not topic_id:
        return Response.fail(code=500, msg="回复ID不能为空")

    condition = {"id": topic_id}

    try:
        # Note: Physical delete due to lack of is_deleted column
        affected_rows = conn.delete(TABLE_NAME, condition=condition)
        if affected_rows > 0:
            return Response.success(msg="回复删除成功")
        else:
            return Response.fail(code=404, msg="未找到要删除的回复")
    except Exception as e:
        return Response.fail(code=500, msg=f"回复删除失败: {str(e)}")


def get_topic(condition: dict):
    """获取回复信息，允许传入查询条件字典"""
    if not condition or len(condition) == 0:
        return Response.fail(code=500, msg="查询条件不能为空")

    # No is_deleted default

    try:
        result = conn.fetch_rows(TABLE_NAME, condition=condition)
        if result is None or len(result) == 0:
            return Response.fail(code=404, msg="查无此回复信息")
        # 如果是根据唯一ID查询，通常只返回一条记录
        if "id" in condition and len(result) == 1:
             return Response.success(data=result[0]) # 返回单个对象而非列表
        return Response.success(data=result) # 返回列表
    except Exception as e:
        return Response.fail(code=500, msg=f"查询回复失败: {str(e)}")


def get_topic_by_id(topic_id: int):
     """根据ID获取单个回复信息"""
     if not topic_id:
         return Response.fail(code=500, msg="回复ID不能为空")
     return get_topic({"id": topic_id})


def get_topics_for_discussion(discussion_id: int, parent_id: int = None):
    """获取指定论坛的所有回复 (可选按父ID过滤)"""
    if not discussion_id:
        return Response.fail(code=500, msg="论坛ID不能为空")
    condition = {"discussion_id": discussion_id}
    if parent_id is not None:
        condition["parent_id"] = parent_id
    else:
        # Typically fetch top-level comments if parent_id is not specified
        condition["parent_id"] = None # Or however NULL is represented
    return get_topic(condition)

# Add function to get child replies for a given parent_id if needed
# def get_child_topics(parent_id: int): ... 