#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from unittest.mock import patch, MagicMock

from app.services import db_services
from app.utils.result_type import Response

mock_conn = MagicMock()

# 注意：如果您通过别名测试，则路径需要包含别名
@patch('app.services.db_services.user_mapping.conn', mock_conn)
class TestUserMappingService(unittest.TestCase):

    def setUp(self):
        mock_conn.reset_mock()

    def test_add_mapping_success(self):
        """测试成功添加用户-论坛映射关系。"""
        mapping_data = {'user_id': 1, 'discuss_id': 10}
        # 模拟映射不存在
        mock_conn.count.return_value = 0
        # 模拟成功插入并返回ID 25
        mock_conn.insert.return_value = 25

        response = db_services.add_mapping(mapping_data)

        # 检查是否执行了存在性检查
        mock_conn.count.assert_called_once_with(
            'user_mapping', condition={'user_id': 1, 'discuss_id': 10, 'is_deleted': 0}
        )
        # 检查 insert 是否被调用
        mock_conn.insert.assert_called_once()
        # 检查插入参数是否包含时间戳和 is_deleted=0
        call_args = mock_conn.insert.call_args[0][1]
        self.assertIn('created_time', call_args)
        self.assertIn('update_time', call_args)
        self.assertEqual(call_args.get('is_deleted'), 0)

        self.assertTrue(response.success)
        self.assertEqual(response.data, {"id": 25})

    def test_add_mapping_already_exists(self):
        """测试添加已存在的映射关系。"""
        mapping_data = {'user_id': 1, 'discuss_id': 10}
        # 模拟映射已存在
        mock_conn.count.return_value = 1

        response = db_services.add_mapping(mapping_data)

        mock_conn.count.assert_called_once_with(
            'user_mapping', condition={'user_id': 1, 'discuss_id': 10, 'is_deleted': 0}
        )
        mock_conn.insert.assert_not_called()
        self.assertFalse(response.success)
        self.assertEqual(response.code, 409) # 冲突
        self.assertEqual(response.msg, "映射关系已存在")

    def test_add_mapping_missing_field(self):
        """测试添加映射关系时缺少 user_id。"""
        mapping_data = {'discuss_id': 10}
        response = db_services.add_mapping(mapping_data)
        self.assertFalse(response.success)
        self.assertEqual(response.code, 500)
        self.assertIn("user_id 不能为空", response.msg)
        mock_conn.count.assert_not_called()
        mock_conn.insert.assert_not_called()

    def test_delete_mapping_by_id_success(self):
        """测试逻辑删除映射关系成功。"""
        mapping_id = 25
        mock_conn.update.return_value = 1 # 模拟影响1行

        # 如果直接测试，则使用别名前的原始函数名
        response = db_services.delete_mapping_by_id(mapping_id)

        mock_conn.update.assert_called_once()
        # 检查逻辑删除的参数
        call_args = mock_conn.update.call_args[0][1]
        call_kwargs = mock_conn.update.call_args[1]
        self.assertEqual(call_args.get('is_deleted'), 1)
        self.assertIn('update_time', call_args)
        self.assertEqual(call_kwargs['condition'], {'id': mapping_id})
        self.assertTrue(response.success)

    def test_check_mapping_exists_true(self):
        """测试检查映射关系是否存在 (True 情况)。"""
        user_id = 1
        discuss_id = 10
        mock_conn.count.return_value = 1
        response = db_services.check_mapping_exists(user_id, discuss_id)
        mock_conn.count.assert_called_once_with(
            'user_mapping', condition={'user_id': 1, 'discuss_id': 10, 'is_deleted': 0}
        )
        self.assertTrue(response.success)
        self.assertTrue(response.data)

    def test_check_mapping_exists_false(self):
        """测试检查映射关系是否存在 (False 情况)。"""
        user_id = 1
        discuss_id = 11
        mock_conn.count.return_value = 0
        response = db_services.check_mapping_exists(user_id, discuss_id)
        mock_conn.count.assert_called_once_with(
            'user_mapping', condition={'user_id': 1, 'discuss_id': 11, 'is_deleted': 0}
        )
        self.assertTrue(response.success)
        self.assertFalse(response.data)

    def test_get_discussions_for_user(self):
        """测试获取指定用户的论坛ID。"""
        user_id = 1
        expected_ids = [10, 15, 20]
        mock_conn.fetch_rows.return_value = [{'discuss_id': 10}, {'discuss_id': 15}, {'discuss_id': 20}]

        response = db_services.get_discussions_for_user(user_id)

        mock_conn.fetch_rows.assert_called_once_with(
            'user_mapping', condition={'user_id': user_id, 'is_deleted': 0}, fields=['discuss_id']
        )
        self.assertTrue(response.success)
        self.assertEqual(response.data, expected_ids)

    def test_get_users_for_discussion(self):
        """测试获取指定论坛的用户ID。"""
        discuss_id = 10
        expected_ids = [1, 5]
        mock_conn.fetch_rows.return_value = [{'user_id': 1}, {'user_id': 5}]

        response = db_services.get_users_for_discussion(discuss_id)

        mock_conn.fetch_rows.assert_called_once_with(
            'user_mapping', condition={'discuss_id': discuss_id, 'is_deleted': 0}, fields=['user_id']
        )
        self.assertTrue(response.success)
        self.assertEqual(response.data, expected_ids)


if __name__ == '__main__':
    unittest.main() 