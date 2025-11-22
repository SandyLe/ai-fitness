#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fitenss_items
@File    ：user_plan.py
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

TABLE_NAME = "user_plan"


def add_plan(plan_data: dict):
    """增加用户计划"""
    if not plan_data or len(plan_data) == 0:
        return Response.fail(code=500, msg="提交信息为空")

    # 必填字段校验
    required_fields = ['user_id', 'plan']
    for field in required_fields:
        if field not in plan_data or not plan_data.get(field):
             # Check for 0 explicitly if needed
             if plan_data.get(field) is None:
                 return Response.fail(code=500, msg=f"字段 {field} 不能为空")

    # 准备插入的数据
    insert_data = plan_data.copy()
    now = datetime.now()
    insert_data['created_time'] = now
    insert_data['update_time'] = now
    insert_data.setdefault('is_deleted', 0)
    # created_by and update_by should ideally be set based on logged-in user context

    try:
        result_id = conn.insert(TABLE_NAME, insert_data)
        return Response.success(data={"id": result_id})
    except Exception as e:
        return Response.fail(code=500, msg=f"创建用户计划失败: {str(e)}")


def update_plan(plan_id: int, update_data: dict):
    """根据ID修改用户计划信息 (e.g., context, plan)"""
    if not plan_id:
        return Response.fail(code=500, msg="计划ID不能为空")
    if not update_data or len(update_data) == 0:
        return Response.fail(code=500, msg="更新信息为空")

    # 不允许修改主键或用户ID
    for forbidden_key in ['id', 'user_id']:
         if forbidden_key in update_data:
             del update_data[forbidden_key]

    if not update_data:
        return Response.fail(code=400, msg="没有可更新的字段")

    # 补充更新时间
    update_data['update_time'] = datetime.now()
    # update_by should be set based on context

    condition = {"id": plan_id, "is_deleted": 0} # 只能更新未删除的

    try:
        affected_rows = conn.update(TABLE_NAME, update_data, condition=condition)
        if affected_rows > 0:
            return Response.success(msg="用户计划更新成功")
        else:
            return Response.fail(code=404, msg="未找到用户计划或无需更新")
    except Exception as e:
        return Response.fail(code=500, msg=f"用户计划更新失败: {str(e)}")


def delete_plan_by_id(plan_id: int):
    """根据ID删除用户计划 (逻辑删除)"""
    if not plan_id:
        return Response.fail(code=500, msg="计划ID不能为空")

    update_data = {
        "is_deleted": 1,
        "update_time": datetime.now()
        # update_by should be set based on context
    }
    condition = {"id": plan_id}

    try:
        affected_rows = conn.update(TABLE_NAME, update_data, condition=condition)
        if affected_rows > 0:
            return Response.success(msg="用户计划删除成功")
        else:
            return Response.fail(code=404, msg="未找到要删除的用户计划或无需更新")
    except Exception as e:
        return Response.fail(code=500, msg=f"用户计划删除失败: {str(e)}")


def get_plan(condition: dict):
    """获取用户计划信息，允许传入查询条件字典，默认只查询未删除的"""
    if not condition or len(condition) == 0:
        return Response.fail(code=500, msg="查询条件不能为空")

    # 默认查询未删除的
    condition.setdefault('is_deleted', 0)

    try:
        result = conn.fetch_rows(TABLE_NAME, condition=condition)
        if result is None or len(result) == 0:
            return Response.fail(code=404, msg="查无此用户计划信息")
        # 如果是根据唯一ID查询，通常只返回一条记录
        if "id" in condition and len(result) == 1:
             return Response.success(data=result[0]) # 返回单个对象而非列表
        return Response.success(data=result) # 返回列表
    except Exception as e:
        return Response.fail(code=500, msg=f"查询用户计划失败: {str(e)}")


def get_plan_by_id(plan_id: int):
     """根据ID获取单个用户计划信息"""
     if not plan_id:
         return Response.fail(code=500, msg="计划ID不能为空")
     return get_plan({"id": plan_id})


def get_plans_for_user(user_id: int):
    """获取指定用户的所有计划 (未删除的)"""
    if not user_id:
        return Response.fail(code=500, msg="用户ID不能为空")
    condition = {"user_id": user_id, "is_deleted": 0}
    return get_plan(condition)


def get_active_plan_for_user(user_id: int):
    """获取指定用户的所有计划 (未删除的)"""
    if not user_id:
        return Response.fail(code=500, msg="用户ID不能为空")
    condition = {"user_id": user_id, "is_deleted": 2}
    return get_plan(condition)