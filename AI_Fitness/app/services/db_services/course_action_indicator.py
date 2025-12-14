#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fitenss_items
@File    ：course_action_indicator.py
@IDE     ：PyCharm
@Author  ：写BUG的Botter
@Date    ：2025/4/12
'''
from datetime import datetime

from app.config import DB_CONFIG
from app.utils.libmysql import MYSQL
from app.utils.result_type import Response
import time

conn = MYSQL(
    dbhost=DB_CONFIG['host'],
    dbuser=DB_CONFIG['user'],
    dbpwd=DB_CONFIG['password'],
    dbname=DB_CONFIG['database'],
    dbport=DB_CONFIG['port'],
    dbcharset='utf8'
)

TABLE_NAME = "course_action_indicator"


def add_action_indicator(action_indicator: dict):
    """增加用户动作结果评价"""
    if not action_indicator or len(action_indicator) == 0:
        return Response.fail(code=500, msg="提交信息为空")

    # 必填字段校验 (user_id. 'data' field in DDL likely means clock-in time)
    required_fields = ['user_id'] # Assuming 'data' is the clock-in timestamp
    for field in required_fields:
        if field not in action_indicator or not action_indicator.get(field):
             if action_indicator.get(field) is None:
                 return Response.fail(code=500, msg=f"字段 {field} 不能为空")

    # 准备插入的数据
    insert_data = action_indicator.copy()
    # Rename 'data' to 'clock_time' internally if desired, but insert with 'data'
    # insert_data['clock_time'] = insert_data.pop('data')

    # now = datetime.now()
    # insert_data['created_time'] = now
    # insert_data['update_time'] = now # Typo in DDL? update_time, not updated_time
    # created_by and update_by should ideally be set based on logged-in user context
    # No is_deleted field in DDL

    try:
        result_id = conn.insert(TABLE_NAME, insert_data)
        return Response.success(data={"result_id": result_id})
    except Exception as e:
        # Check for duplicate entry if user_id + date is unique constraint
        return Response.fail(code=500, msg=f"创建动作结果评价失败: {str(e)}")

# Update doesn't make much sense unless updating audit fields or maybe the clock_time itself
# def update_action_indicator(record_id: int, update_data: dict): ...

def delete_action_indicator_by_id(record_id: int):
    """根据ID删除动作结果评价 (物理删除)"""
    if not record_id:
        return Response.fail(code=500, msg="动作结果评价ID不能为空")

    condition = {"record_id": record_id}

    try:
        # Note: Physical delete due to lack of is_deleted column
        affected_rows = conn.delete(TABLE_NAME, condition=condition)
        if affected_rows > 0:
            return Response.success(msg="动作结果评价删除成功")
        else:
            return Response.fail(code=404, msg="未找到要删除的动作结果评价")
    except Exception as e:
        return Response.fail(code=500, msg=f"动作结果评价删除失败: {str(e)}")


def get_action_indicator(condition: dict):
    """获取动作结果评价，允许传入查询条件字典"""
    if not condition or len(condition) == 0:
        return Response.fail(code=500, msg="查询条件不能为空")

    try:
        result = conn.fetch_rows(TABLE_NAME, condition=condition)
        if result is None or len(result) == 0:
            return Response.fail(code=404, msg="查无此动作结果评价")
        # 如果是根据唯一ID查询，通常只返回一条记录
        if "result_id" in condition and len(result) == 1:
             # Rename 'data' field if desired in the response
             # single_result = result[0]
             # single_result['clock_time'] = single_result.pop('data')
             # return Response.success(data=single_result)
             return Response.success(data=result[0])
        # Rename 'data' field in list response if desired
        # for row in result:
        #     row['clock_time'] = row.pop('data')
        return Response.success(data=result) # 返回列表
    except Exception as e:
        return Response.fail(code=500, msg=f"查询动作结果评价失败: {str(e)}")


def get_action_indicator_by_id(record_id: int):
     """根据ID获取单个动作结果评价"""
     if not record_id:
         return Response.fail(code=500, msg="动作结果评价ID不能为空")
     return get_action_indicator({"id": record_id})

