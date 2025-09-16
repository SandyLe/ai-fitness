#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fitenss_items
@File    ：user_plan_date_mapping.py
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
    dbcharset='utf8'
)

TABLE_NAME = "user_plan_date_mapping"


def add_plan_date_mapping(mapping_data: dict):
    """增加用户计划-数据映射关系"""
    if not mapping_data or len(mapping_data) == 0:
        return Response.fail(code=500, msg="提交信息为空")

    # 必填字段校验
    required_fields = ['data_id', 'plan_id'] # Referring to user_date.id and user_plan.id
    for field in required_fields:
        if field not in mapping_data or not mapping_data.get(field):
             if mapping_data.get(field) is None:
                 return Response.fail(code=500, msg=f"字段 {field} 不能为空")

    # 检查是否已存在 (避免重复映射)
    exists_check = check_mapping_exists(mapping_data['data_id'], mapping_data['plan_id'])
    if exists_check.success and exists_check.data:
         return Response.fail(code=409, msg="映射关系已存在")

    # 准备插入的数据
    insert_data = mapping_data.copy()
    now = datetime.now()
    insert_data['created_time'] = now
    insert_data['update_time'] = now
    # created_by and update_by should ideally be set based on logged-in user context
    # No is_deleted field in DDL

    try:
        result_id = conn.insert(TABLE_NAME, insert_data)
        return Response.success(data={"id": result_id})
    except Exception as e:
        return Response.fail(code=500, msg=f"创建计划数据映射失败: {str(e)}")


def delete_mapping_by_id(mapping_id: int):
    """根据ID删除映射关系 (物理删除)"""
    if not mapping_id:
        return Response.fail(code=500, msg="映射ID不能为空")

    condition = {"id": mapping_id}

    try:
        # Note: Physical delete due to lack of is_deleted column
        affected_rows = conn.delete(TABLE_NAME, condition=condition)
        if affected_rows > 0:
            return Response.success(msg="映射关系删除成功")
        else:
            return Response.fail(code=404, msg="未找到要删除的映射关系")
    except Exception as e:
        return Response.fail(code=500, msg=f"删除映射关系失败: {str(e)}")

# Update function omitted as it's usually not needed for mapping tables.

def get_mapping(condition: dict):
    """获取映射关系，允许传入查询条件字典"""
    if not condition or len(condition) == 0:
        return Response.fail(code=500, msg="查询条件不能为空")

    # No is_deleted default

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

def check_mapping_exists(data_id: int, plan_id: int):
    """检查指定数据和计划的映射是否存在"""
    if not data_id or not plan_id:
        return Response.fail(code=500, msg="数据ID和计划ID均不能为空")
    condition = {
        "data_id": data_id,
        "plan_id": plan_id
        # No is_deleted check
    }
    try:
        count = conn.count(TABLE_NAME, condition=condition)
        return Response.success(data=(count > 0))
    except Exception as e:
        return Response.fail(code=500, msg=f"检查映射关系失败: {str(e)}")

def get_plans_for_data(data_id: int):
    """获取指定数据关联的所有计划ID"""
    if not data_id:
        return Response.fail(code=500, msg="数据ID不能为空")
    condition = {"data_id": data_id}
    try:
        # 只选择 plan_id 字段
        results = conn.fetch_rows(TABLE_NAME, condition=condition, fields=['plan_id'])
        plan_ids = [row['plan_id'] for row in results]
        return Response.success(data=plan_ids)
    except Exception as e:
        return Response.fail(code=500, msg=f"查询数据关联的计划失败: {str(e)}")

def get_data_for_plan(plan_id: int):
    """获取指定计划关联的所有数据ID"""
    if not plan_id:
        return Response.fail(code=500, msg="计划ID不能为空")
    condition = {"plan_id": plan_id}
    try:
        # 只选择 data_id 字段
        results = conn.fetch_rows(TABLE_NAME, condition=condition, fields=['data_id'])
        data_ids = [row['data_id'] for row in results]
        return Response.success(data=data_ids)
    except Exception as e:
        return Response.fail(code=500, msg=f"查询计划关联的数据失败: {str(e)}") 