# #!/usr/bin/env python
# # -*- coding: UTF-8 -*-
# '''
# @Project ：fitenss_items
# @File    ：user_info.py
# @IDE     ：PyCharm
# @Author  ：写BUG的Botter
# @Date    ：2025/4/11 08:51
# '''
# from libmysql import MYSQL
# from result_type import Response
# conn = MYSQL(
#         dbhost = '1.95.204.246',
#         dbuser = 'root',
#         dbpwd = 'ZhengHaiBO@123*100',
#         dbname = 'work_out',
#         dbcharset = 'utf8')
# """增加用户"""
# def add_user(user:dict):
#     if user is not None:
#         result_id = conn.insert("user_info", user)
#         return Response.success(dict(id=result_id))
#     else:
#         return Response.fail(code=500,msg="用户为空")
# """删除用户"""
# def del_user(user:dict):
#     if user is not None:
#         result_id = conn.delete("user_info", user ,"2")
#         return Response.success(dict(id=result_id))
#     else:
#         return Response.fail(code=500,msg="用户为空")
# """修改用户"""
# def update_user(user:dict):
#     """修改用户信息，这里必须要传入一个唯一字段，否则会影响相同信息"""
#     if user is not None:
#         result_id = conn.update("user_info", user)
#         return Response.success(dict(id=result_id))
#     else:
#         return Response.fail(code=500,msg="用户为空")
# def get_user_info(user:dict):
#     if user is not None:
#
#         result = conn.fetch_rows("user_info", condition=user)
#         # print(result , result is None , result.count())
#         if len(result) == 0 or result is None:
#             return Response.fail(code=500,msg="查无此人")
#         return Response.success(data=result)
#     else:
#         return Response.fail(code=500,msg="未知错误")
# # user = {
# #     "user_name":"Botter",
# #     "password":"123456"
# # }
# # print(add_user(user))
# # print(add_user(None))
#
# # print(get_user_info({"user_name":"Botter"}))
# # print(get_user_info({"id": 1}))
# # user = {
# #     "user_name":"zzz",
# #     "password":"23456"
# # }
# # print(update_user(user))
#
