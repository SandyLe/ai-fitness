#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fitenss_items
@File    ：user_question_answer.py
@IDE     ：PyCharm
@Author  ：sandylee
@Date    ：2025/11/29
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

TABLE_NAME = "user_question_answer"


def add_question_answer(user_question_answer: dict):
    """增加用户用户问题答案记录"""
    if not user_question_answer or len(user_question_answer) == 0:
        return Response.fail(code=500, msg="提交信息为空")

    # 必填字段校验 (user_id. 'data' field in DDL likely means user_question_answer time)
    required_fields = ['user_id', 'question_id', 'question_answer'] # Assuming 'data' is the user_question_answer timestamp
    for field in required_fields:
        if field not in user_question_answer or not user_question_answer.get(field):
             if user_question_answer.get(field) is None:
                 return Response.fail(code=500, msg=f"字段 {field} 不能为空")

    # 准备插入的数据
    insert_data = user_question_answer.copy()
    # Rename 'data' to 'user_question_answer' internally if desired, but insert with 'data'
    # insert_data['user_question_answer'] = insert_data.pop('data')

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
        return Response.fail(code=500, msg=f"创建用户问题答案记录失败: {str(e)}")


def delete_question_answer_by_id(id: int):
    """根据ID删除用户问题答案记录 (物理删除)"""
    if not id:
        return Response.fail(code=500, msg="用户问题答案记录ID不能为空")

    condition = {"id": id}

    try:
        # Note: Physical delete due to lack of is_deleted column
        affected_rows = conn.delete(TABLE_NAME, condition=condition)
        if affected_rows > 0:
            return Response.success(msg="用户问题答案记录删除成功")
        else:
            return Response.fail(code=404, msg="未找到要删除的用户问题答案记录")
    except Exception as e:
        return Response.fail(code=500, msg=f"用户问题答案记录删除失败: {str(e)}")


def get_question_answer(condition: dict):
    """获取用户问题答案记录，允许传入查询条件字典"""
    if not condition or len(condition) == 0:
        return Response.fail(code=500, msg="查询条件不能为空")

    # No is_deleted default

    try:
        result = conn.fetch_rows(TABLE_NAME, condition=condition)
        if result is None or len(result) == 0:
            return Response.fail(code=404, msg="查无此用户问题答案记录")
        # 如果是根据唯一ID查询，通常只返回一条记录
        if "id" in condition and len(result) == 1:
             return Response.success(data=result[0])
        return Response.success(data=result) # 返回列表
    except Exception as e:
        return Response.fail(code=500, msg=f"查询用户问题答案记录失败: {str(e)}")


def get_question_answer_by_id(id: int):
     """根据ID获取单个用户问题答案记录"""
     if not id:
         return Response.fail(code=500, msg="用户问题答案记录ID不能为空")
     return get_question_answer({"id": id})


def get_question_answers_for_user(user_id: int, start_date=None, end_date=None):
    """获取指定用户的所有用户问题答案记录 (可选日期范围)"""
    if not user_id:
        return Response.fail(code=500, msg="用户ID不能为空")
    condition = {"user_id": user_id}
    # Add date range filtering on the 'data' column if needed
    # Example requires specific implementation in libmysql or raw SQL
    # if start_date:
    #     condition['data_gte'] = start_date # Placeholder for actual condition
    # if end_date:
    #     condition['data_lte'] = end_date   # Placeholder for actual condition

    return get_question_answer(condition)

def get_question_answers_for_user_date(user_id: int, start_date=None, end_date=None):
    """获取指定用户的所有用户问题答案记录 (可选日期范围)"""
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
    condition = 'user_id = {} AND (data > \'{}\') AND data < \'{}\' limit 1'.format(user_id, start_time, end_time)
    return get_question_answer(condition)

def count_question_answer(user_id: int, start_date=None, end_date=None):
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
        return Response.success(data=result) # 返回列表
    except Exception as e:
        return Response.fail(code=500, msg=f"查询用户问题答案记录失败: {str(e)}")
