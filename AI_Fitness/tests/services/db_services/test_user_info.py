#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from unittest.mock import patch, MagicMock

# 假设您的服务可以这样导入
from app.services import db_services
from app.utils.result_type import Response # 假设 Response 结构

# 在此模块的所有测试中全局模拟数据库连接
# 您可能需要根据 'conn' 在每个服务文件中的实际定义位置调整目标字符串
# (例如 'app.services.db_services.user_info.conn')
mock_conn = MagicMock()

@patch('app.services.db_services.user_info.conn', mock_conn)
class TestUserInfoService(unittest.TestCase):

    def setUp(self):
        # 在每个测试前重置模拟对象
        mock_conn.reset_mock()

    def test_add_user_success(self):
        """测试成功添加用户。"""
        user_data = {'user_name': 'testuser', 'password': 'pass123', 'weight': 70, 'email': 'test@example.com'}
        mock_conn.insert.return_value = 1 # 模拟成功插入并返回ID 1
        mock_conn.count.return_value = 0 # 模拟用户名不存在

        response = db_services.add_user(user_data)

        mock_conn.count.assert_called_once_with(table='user_info', condition={'user_name': 'testuser', 'is_deleted': 0})
        mock_conn.insert.assert_called_once()
        # 如果需要，可以更具体地断言插入参数
        self.assertTrue(response.success)
        self.assertEqual(response.code, 200)
        self.assertEqual(response.data, {"id": 1})

    def test_add_user_missing_field(self):
        """测试添加用户时缺少必需字段。"""
        user_data = {'user_name': 'testuser'} # 缺少 password 和 weight
        response = db_services.add_user(user_data)
        self.assertFalse(response.success)
        self.assertEqual(response.code, 500)
        self.assertIn("不能为空", response.msg)
        mock_conn.insert.assert_not_called()

    def test_add_user_duplicate_username(self):
        """测试添加已存在的用户名。"""
        user_data = {'user_name': 'existinguser', 'password': 'pass123', 'weight': 70}
        mock_conn.count.return_value = 1 # 模拟用户名已存在

        response = db_services.add_user(user_data)

        mock_conn.count.assert_called_once_with(table='user_info', condition={'user_name': 'existinguser', 'is_deleted': 0})
        self.assertFalse(response.success)
        self.assertEqual(response.code, 500)
        self.assertEqual(response.msg, "用户名已存在！")
        mock_conn.insert.assert_not_called()

    def test_get_user_by_id_success(self):
        """测试通过ID成功获取用户。"""
        user_id = 1
        expected_user = {'id': user_id, 'user_name': 'testuser', 'weight': 70, 'is_deleted': 0}
        mock_conn.fetch_rows.return_value = [expected_user] # 模拟找到用户

        response = db_services.get_user_by_id(user_id)

        mock_conn.fetch_rows.assert_called_once_with('user_info', condition={'id': user_id, 'is_deleted': 0})
        self.assertTrue(response.success)
        self.assertEqual(response.data, expected_user)

    def test_get_user_by_id_not_found(self):
        """测试通过不存在的ID获取用户。"""
        user_id = 999
        mock_conn.fetch_rows.return_value = [] # 模拟未找到用户

        response = db_services.get_user_by_id(user_id)

        mock_conn.fetch_rows.assert_called_once_with('user_info', condition={'id': user_id, 'is_deleted': 0})
        self.assertFalse(response.success)
        self.assertEqual(response.code, 404)
        self.assertEqual(response.msg, "查无此用户")

    def test_update_user_success(self):
        """测试成功更新用户。"""
        user_id = 1
        update_data = {'nick_name': 'New Nickname', 'height': 180}
        mock_conn.update.return_value = 1 # 模拟影响1行

        response = db_services.update_user(user_id, update_data.copy()) # 传递副本

        mock_conn.update.assert_called_once()
        # 如果需要，断言传递给 update 的具体参数
        # 检查 'updated_time' 是否已添加，以及 'id'/'user_name' 是否不在参数中
        self.assertTrue(response.success)
        self.assertEqual(response.msg, "用户信息更新成功")

    def test_update_user_not_found(self):
        """测试更新不存在的用户。"""
        user_id = 999
        update_data = {'nick_name': 'New Nickname'}
        mock_conn.update.return_value = 0 # 模拟影响0行

        response = db_services.update_user(user_id, update_data)

        mock_conn.update.assert_called_once()
        self.assertFalse(response.success)
        self.assertEqual(response.code, 404)
        self.assertIn("未找到用户或无需更新", response.msg)

    def test_delete_user_by_id_success(self):
        """测试成功逻辑删除用户。"""
        user_id = 1
        mock_conn.update.return_value = 1 # 模拟逻辑删除影响1行

        response = db_services.delete_user_by_id(user_id)

        mock_conn.update.assert_called_once()
        # 断言逻辑删除的具体参数 (is_deleted=1, updated_time)
        self.assertTrue(response.success)
        self.assertEqual(response.msg, "用户删除成功")

    def test_delete_user_by_id_not_found(self):
        """测试删除不存在的用户。"""
        user_id = 999
        mock_conn.update.return_value = 0 # 模拟影响0行

        response = db_services.delete_user_by_id(user_id)

        mock_conn.update.assert_called_once()
        self.assertFalse(response.success)
        self.assertEqual(response.code, 404)
        self.assertIn("未找到要删除的用户或无需更新", response.msg)

if __name__ == '__main__':
    unittest.main() 