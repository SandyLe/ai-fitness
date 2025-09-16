#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

from app.services import db_services
from app.utils.result_type import Response

mock_conn = MagicMock()

@patch('app.services.db_services.user_discussion.conn', mock_conn)
class TestUserDiscussionService(unittest.TestCase):

    def setUp(self):
        mock_conn.reset_mock()

    def test_add_discussion_success(self):
        """测试成功添加论坛讨论。"""
        discussion_data = {'title': 'Test Title', 'content': 'Test content', 'created_by': 1}
        mock_conn.insert.return_value = 5 # 模拟插入返回ID 5

        response = db_services.add_discussion(discussion_data)

        mock_conn.insert.assert_called_once()
        # 检查插入参数是否包含时间戳和 is_deleted=0
        call_args = mock_conn.insert.call_args[0][1] # 获取传递给 insert 的字典
        self.assertEqual(call_args['title'], 'Test Title')
        self.assertIn('created_time', call_args)
        self.assertIn('update_time', call_args)
        self.assertEqual(call_args.get('is_deleted'), 0)

        self.assertTrue(response.success)
        self.assertEqual(response.data, {"id": 5})

    def test_add_discussion_missing_field(self):
        """测试添加论坛讨论时缺少标题字段。"""
        discussion_data = {'content': 'Test content'}
        response = db_services.add_discussion(discussion_data)
        self.assertFalse(response.success)
        self.assertEqual(response.code, 500)
        self.assertIn("字段 title 不能为空", response.msg)
        mock_conn.insert.assert_not_called()

    def test_get_discussion_by_id_success(self):
        """测试通过ID成功获取论坛讨论。"""
        discussion_id = 5
        expected_data = {'id': discussion_id, 'title': 'Test Title', 'is_deleted': 0}
        mock_conn.fetch_rows.return_value = [expected_data]

        response = db_services.get_discussion_by_id(discussion_id)

        mock_conn.fetch_rows.assert_called_once_with(
            'user_discussion', condition={'id': discussion_id, 'is_deleted': 0}
        )
        self.assertTrue(response.success)
        self.assertEqual(response.data, expected_data)

    def test_get_discussion_by_id_not_found(self):
        """测试获取不存在的论坛讨论。"""
        discussion_id = 99
        mock_conn.fetch_rows.return_value = []
        response = db_services.get_discussion_by_id(discussion_id)
        self.assertFalse(response.success)
        self.assertEqual(response.code, 404)

    def test_update_discussion_success(self):
        """测试成功更新论坛讨论。"""
        discussion_id = 5
        update_data = {'content': 'Updated content'}
        mock_conn.update.return_value = 1 # 影响1行

        response = db_services.update_discussion(discussion_id, update_data.copy())

        mock_conn.update.assert_called_once()
        # 检查 update_time 参数
        call_args = mock_conn.update.call_args[0][1] # 数据字典
        call_kwargs = mock_conn.update.call_args[1] # 关键字参数 (condition)
        self.assertIn('update_time', call_args)
        self.assertEqual(call_kwargs['condition'], {'id': discussion_id, 'is_deleted': 0})
        self.assertTrue(response.success)

    def test_delete_discussion_by_id_success(self):
        """测试逻辑删除论坛讨论成功。"""
        discussion_id = 5
        mock_conn.update.return_value = 1 # 影响1行

        response = db_services.delete_discussion_by_id(discussion_id)

        mock_conn.update.assert_called_once()
        # 检查逻辑删除的参数 (is_deleted=1, update_time)
        call_args = mock_conn.update.call_args[0][1] # 数据字典
        call_kwargs = mock_conn.update.call_args[1] # 关键字参数 (condition)
        self.assertEqual(call_args.get('is_deleted'), 1)
        self.assertIn('update_time', call_args)
        self.assertEqual(call_kwargs['condition'], {'id': discussion_id})
        self.assertTrue(response.success)

    def test_count_discussions(self):
        """测试统计论坛讨论数量。"""
        mock_conn.count.return_value = 15
        response = db_services.count_discussions()
        mock_conn.count.assert_called_once_with(table='user_discussion', condition={'is_deleted': 0})
        self.assertTrue(response.success)
        self.assertEqual(response.data, 15)

if __name__ == '__main__':
    unittest.main() 