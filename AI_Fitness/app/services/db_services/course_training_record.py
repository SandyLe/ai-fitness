#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fitenss_items
@File    ：course_training_record.py
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

TABLE_NAME = "course_training_record"


def add_training_record(training_record: dict):
    """增加用户训练记录"""
    if not training_record or len(training_record) == 0:
        return Response.fail(code=500, msg="提交信息为空")

    # 必填字段校验 (user_id. 'data' field in DDL likely means clock-in time)
    required_fields = ['user_id'] # Assuming 'data' is the clock-in timestamp
    for field in required_fields:
        if field not in training_record or not training_record.get(field):
             if training_record.get(field) is None:
                 return Response.fail(code=500, msg=f"字段 {field} 不能为空")

    # 准备插入的数据
    insert_data = training_record.copy()
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
        return Response.fail(code=500, msg=f"创建训练记录失败: {str(e)}")

# Update doesn't make much sense unless updating audit fields or maybe the clock_time itself
# def update_training_record(record_id: int, update_data: dict): ...

def delete_training_record_by_id(record_id: int):
    """根据ID删除训练记录 (物理删除)"""
    if not record_id:
        return Response.fail(code=500, msg="训练记录ID不能为空")

    condition = {"record_id": record_id}

    try:
        # Note: Physical delete due to lack of is_deleted column
        affected_rows = conn.delete(TABLE_NAME, condition=condition)
        if affected_rows > 0:
            return Response.success(msg="训练记录删除成功")
        else:
            return Response.fail(code=404, msg="未找到要删除的训练记录")
    except Exception as e:
        return Response.fail(code=500, msg=f"训练记录删除失败: {str(e)}")


def get_training_record(condition: dict):
    """获取训练记录，允许传入查询条件字典"""
    if not condition or len(condition) == 0:
        return Response.fail(code=500, msg="查询条件不能为空")

    # No is_deleted default

    try:
        result = conn.fetch_rows(TABLE_NAME, condition=condition)
        if result is None or len(result) == 0:
            return Response.fail(code=404, msg="查无此训练记录")
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
        return Response.fail(code=500, msg=f"查询训练记录失败: {str(e)}")


def get_training_record_by_id(record_id: int):
     """根据ID获取单个训练记录"""
     if not record_id:
         return Response.fail(code=500, msg="训练记录ID不能为空")
     return get_training_record({"id": record_id})


def get_training_records_for_user(user_id: int, start_date=None, end_date=None):
    """获取指定用户的所有训练记录 (可选日期范围)"""
    if not user_id:
        return Response.fail(code=500, msg="用户ID不能为空")
    condition = {"user_id": user_id}
    # Add date range filtering on the 'data' column if needed
    # Example requires specific implementation in libmysql or raw SQL
    # if start_date:
    #     condition['data_gte'] = start_date # Placeholder for actual condition
    # if end_date:
    #     condition['data_lte'] = end_date   # Placeholder for actual condition

    return get_training_record(condition)

def get_training_records_for_user_date(user_id: int, start_date=None, end_date=None):
    """获取指定用户的所有训练记录 (可选日期范围)"""
    if not user_id:
        return Response.fail(code=500, msg="用户ID不能为空")
    # condition = {"user_id": user_id}
    # Add date range filtering on the 'data' column if needed
    # Example requires specific implementation in libmysql or raw SQL
    # if start_date:
    #     condition['data_gte'] = start_date # Placeholder for actual condition
    # if end_date:
    #     condition['data_lte'] = end_date   # Placeholder for actual condition
    start_time = time.strftime("%Y-%m-%d", time.localtime(start_date)) + ' 00:00:00'
    end_time = time.strftime("%Y-%m-%d", time.localtime(end_date)) + ' 23:59:59'
    condition = 'user_id = {} AND (start_time > \'{}\') AND start_time < \'{}\' limit 1'.format(user_id, start_time, end_time)
    return get_training_record(condition)

def count_training_record(user_id: int, start_date=None, end_date=None):
    condition = 'user_id = {} '.format(user_id)
    if (start_date is not None) :
        start_time = time.strftime("%Y-%m-%d", time.localtime(start_date)) + ' 00:00:00'
        condition = condition + ' AND (data > \'{}\') '.format(start_time)
    if (end_date is not None) :
       end_time = time.strftime("%Y-%m-%d", time.localtime(end_date)) + ' 23:59:59'
       condition = condition + ' AND (data < \'{}\') '.format(end_time)

    if not condition or len(condition) == 0:
        return Response.fail(code=500, msg="查询条件不能为空")
    try:
        result = conn.count(TABLE_NAME, condition=condition)
        # Rename 'data' field in list response if desired
        # for row in result:
        #     row['clock_time'] = row.pop('data')
        return Response.success(data=result) # 返回列表
    except Exception as e:
        return Response.fail(code=500, msg=f"查询训练记录失败: {str(e)}")
