#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fitenss_items
@File    ：user_mapping.py
@IDE     ：PyCharm
@Author  ：写BUG的Botter
@Date    ：2025/4/11 08:51
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

TABLE_NAME = "user_mapping"


def add_mapping(mapping_data: dict):
    """增加用户-论坛映射关系"""
    # 基础校验
    if not mapping_data or len(mapping_data) == 0:
        return Response.fail(code=500, msg="提交信息为空")

    # 必填字段校验
    required_fields = ['user_id', 'discuss_id']
    for field in required_fields:
        if field not in mapping_data or not mapping_data.get(field):
            return Response.fail(code=500, msg=f"字段 {field} 不能为空")

    # 检查是否已存在 (避免重复映射)
    exists_check = check_mapping_exists(mapping_data['user_id'], mapping_data['discuss_id'])
    if exists_check.success and exists_check.data:
         return Response.fail(code=409, msg="映射关系已存在")

    # 准备插入的数据
    insert_data = mapping_data.copy()
    now = datetime.now()
    insert_data['created_time'] = now
    insert_data['update_time'] = now
    insert_data.setdefault('is_deleted', 0)
    # created_by 和 update_by 应根据上下文设置

    try:
        result_id = conn.insert(TABLE_NAME, insert_data)
        return Response.success(data={"id": result_id})
    except Exception as e:
        return Response.fail(code=500, msg=f"创建映射关系失败: {str(e)}")


def delete_mapping_by_id(mapping_id: int):
    """根据ID删除映射关系 (逻辑删除)"""
    if not mapping_id:
        return Response.fail(code=500, msg="映射ID不能为空")

    update_data = {
        "is_deleted": 1,
        "update_time": datetime.now()
        # update_by should be set based on context
    }
    condition = {"id": mapping_id}

    try:
        affected_rows = conn.update(TABLE_NAME, update_data, condition=condition)
        if affected_rows > 0:
            return Response.success(msg="映射关系删除成功")
        else:
            return Response.fail(code=404, msg="未找到要删除的映射关系或无需更新")
    except Exception as e:
        return Response.fail(code=500, msg=f"删除映射关系失败: {str(e)}")


def update_mapping(mapping_id: int, update_data: dict):
    """根据ID修改映射关系 (注意：通常不修改user_id或discuss_id)"""
    if not mapping_id:
        return Response.fail(code=500, msg="映射ID不能为空")
    if not update_data or len(update_data) == 0:
        return Response.fail(code=500, msg="更新信息为空")

    # 不允许修改关联外键或主键
    for forbidden_key in ['id', 'user_id', 'discuss_id']:
         if forbidden_key in update_data:
             del update_data[forbidden_key]

    if not update_data: # 如果不允许修改的字段被移除后为空
        return Response.fail(code=400, msg="没有可更新的字段")

    # 补充更新时间
    update_data['update_time'] = datetime.now()
    # update_by should be set based on context

    condition = {"id": mapping_id, "is_deleted": 0} # 只能更新未删除的

    try:
        affected_rows = conn.update(TABLE_NAME, update_data, condition=condition)
        if affected_rows > 0:
            return Response.success(msg="映射关系更新成功")
        else:
            return Response.fail(code=404, msg="未找到映射关系或无需更新")
    except Exception as e:
        return Response.fail(code=500, msg=f"更新映射关系失败: {str(e)}")


def get_mapping(condition: dict):
    """获取映射关系，允许传入查询条件字典，默认只查询未删除的"""
    if not condition or len(condition) == 0:
        return Response.fail(code=500, msg="查询条件不能为空")

    # 默认查询未删除的
    condition.setdefault('is_deleted', 0)

    try:
        result = conn.fetch_rows(TABLE_NAME, condition=condition)
        if result is None or len(result) == 0:
            return Response.fail(code=404, msg="查无此映射关系")
        # 如果是根据唯一ID查询，通常只返回一条记录
        if "id" in condition and len(result) == 1:
             return Response.success(data=result[0]) # 返回单个对象而非列表
        return Response.success(data=result) # 返回列表
    except Exception as e:
        return Response.fail(code=500, msg=f"查询映射关系失败: {str(e)}")

def get_mapping_by_id(mapping_id: int):
     """根据ID获取单个映射关系"""
     if not mapping_id:
         return Response.fail(code=500, msg="映射ID不能为空")
     return get_mapping({"id": mapping_id})

def check_mapping_exists(user_id: int, discuss_id: int):
    """检查指定用户和论坛的映射是否存在 (未删除的)"""
    if not user_id or not discuss_id:
        return Response.fail(code=500, msg="用户ID和论坛ID均不能为空")
    condition = {
        "user_id": user_id,
        "discuss_id": discuss_id,
        "is_deleted": 0
    }
    try:
        count = conn.count(TABLE_NAME, condition=condition)
        return Response.success(data=(count > 0))
    except Exception as e:
        return Response.fail(code=500, msg=f"检查映射关系失败: {str(e)}")

def get_discussions_for_user(user_id: int):
    """获取指定用户关联的所有论坛ID (未删除的映射)"""
    if not user_id:
        return Response.fail(code=500, msg="用户ID不能为空")
    condition = {"user_id": user_id, "is_deleted": 0}
    try:
        # 只选择 discuss_id 字段
        results = conn.fetch_rows(TABLE_NAME, condition=condition, fields=['discuss_id'])
        discuss_ids = [row['discuss_id'] for row in results]
        return Response.success(data=discuss_ids)
    except Exception as e:
        return Response.fail(code=500, msg=f"查询用户关联的论坛失败: {str(e)}")

def get_users_for_discussion(discuss_id: int):
    """获取指定论坛关联的所有用户ID (未删除的映射)"""
    if not discuss_id:
        return Response.fail(code=500, msg="论坛ID不能为空")
    condition = {"discuss_id": discuss_id, "is_deleted": 0}
    try:
        # 只选择 user_id 字段
        results = conn.fetch_rows(TABLE_NAME, condition=condition, fields=['user_id'])
        user_ids = [row['user_id'] for row in results]
        return Response.success(data=user_ids)
    except Exception as e:
        return Response.fail(code=500, msg=f"查询论坛关联的用户失败: {str(e)}")
