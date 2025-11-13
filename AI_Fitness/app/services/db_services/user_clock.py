#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fitenss_items
@File    ：user_clock.py
@IDE     ：PyCharm
@Author  ：写BUG的Botter
@Date    ：2025/4/12
'''
from datetime import datetime

from sympy.strategies.branch import condition

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

TABLE_NAME = "user_clock"


def add_clock_in(clock_data: dict):
    """增加用户打卡记录"""
    if not clock_data or len(clock_data) == 0:
        return Response.fail(code=500, msg="提交信息为空")

    # 必填字段校验 (user_id. 'data' field in DDL likely means clock-in time)
    required_fields = ['user_id', 'data'] # Assuming 'data' is the clock-in timestamp
    for field in required_fields:
        if field not in clock_data or not clock_data.get(field):
             if clock_data.get(field) is None:
                 return Response.fail(code=500, msg=f"字段 {field} 不能为空")

    # 准备插入的数据
    insert_data = clock_data.copy()
    # Rename 'data' to 'clock_time' internally if desired, but insert with 'data'
    # insert_data['clock_time'] = insert_data.pop('data')

    now = datetime.now()
    insert_data['created_time'] = now
    insert_data['update_time'] = now # Typo in DDL? update_time, not updated_time
    # created_by and update_by should ideally be set based on logged-in user context
    # No is_deleted field in DDL

    try:
        result_id = conn.insert(TABLE_NAME, insert_data)
        return Response.success(data={"id": result_id})
    except Exception as e:
        # Check for duplicate entry if user_id + date is unique constraint
        return Response.fail(code=500, msg=f"创建打卡记录失败: {str(e)}")

# Update doesn't make much sense unless updating audit fields or maybe the clock_time itself
# def update_clock_in(clock_id: int, update_data: dict): ...

def delete_clock_in_by_id(clock_id: int):
    """根据ID删除打卡记录 (物理删除)"""
    if not clock_id:
        return Response.fail(code=500, msg="打卡记录ID不能为空")

    condition = {"id": clock_id}

    try:
        # Note: Physical delete due to lack of is_deleted column
        affected_rows = conn.delete(TABLE_NAME, condition=condition)
        if affected_rows > 0:
            return Response.success(msg="打卡记录删除成功")
        else:
            return Response.fail(code=404, msg="未找到要删除的打卡记录")
    except Exception as e:
        return Response.fail(code=500, msg=f"打卡记录删除失败: {str(e)}")


def get_clock_in(condition: dict):
    """获取打卡记录，允许传入查询条件字典"""
    if not condition or len(condition) == 0:
        return Response.fail(code=500, msg="查询条件不能为空")

    # No is_deleted default

    try:
        result = conn.fetch_rows(TABLE_NAME, condition=condition)
        if result is None or len(result) == 0:
            return Response.fail(code=404, msg="查无此打卡记录")
        # 如果是根据唯一ID查询，通常只返回一条记录
        if "id" in condition and len(result) == 1:
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
        return Response.fail(code=500, msg=f"查询打卡记录失败: {str(e)}")


def get_clock_in_by_id(clock_id: int):
     """根据ID获取单个打卡记录"""
     if not clock_id:
         return Response.fail(code=500, msg="打卡记录ID不能为空")
     return get_clock_in({"id": clock_id})


def get_clock_ins_for_user(user_id: int, start_date=None, end_date=None):
    """获取指定用户的所有打卡记录 (可选日期范围)"""
    if not user_id:
        return Response.fail(code=500, msg="用户ID不能为空")
    condition = {"user_id": user_id}
    # Add date range filtering on the 'data' column if needed
    # Example requires specific implementation in libmysql or raw SQL
    # if start_date:
    #     condition['data_gte'] = start_date # Placeholder for actual condition
    # if end_date:
    #     condition['data_lte'] = end_date   # Placeholder for actual condition

    return get_clock_in(condition)

def get_clock_ins_for_user_date(user_id: int, start_date=None, end_date=None):
    """获取指定用户的所有打卡记录 (可选日期范围)"""
    if not user_id:
        return Response.fail(code=500, msg="用户ID不能为空")
    # condition = {"user_id": user_id}
    # Add date range filtering on the 'data' column if needed
    # Example requires specific implementation in libmysql or raw SQL
    # if start_date:
    #     condition['data_gte'] = start_date # Placeholder for actual condition
    # if end_date:
    #     condition['data_lte'] = end_date   # Placeholder for actual condition
    condition = 'user_id = ' + user_id + ' AND data < \'2025-11-14\' limit 1'
    return get_clock_in(condition)