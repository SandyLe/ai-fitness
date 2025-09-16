#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from unittest.mock import patch, MagicMock

from app.services import db_services
from app.utils.result_type import Response

mock_conn = MagicMock()

@patch('app.services.db_services.user_date.conn', mock_conn)
class TestUserDateService(unittest.TestCase):

    def setUp(self):
        mock_conn.reset_mock()

    def test_add_user_score_data_success(self):
        """测试成功添加用户分数数据。"""
        score_data = {'user_id': 1, 'title': 'Day 1 Score', 'score': 100}
        mock_conn.insert.return_value = 401 # 模拟插入ID

        response = db_services.add_user_score_data(score_data)

        mock_conn.insert.assert_called_once()
        call_args = mock_conn.insert.call_args[0][1]
        self.assertEqual(call_args['title'], 'Day 1 Score')
        self.assertIn('created_time', call_args)
        self.assertIn('update_time', call_args)
        # self.assertNotIn('is_deleted', call_args) # 无 is_deleted 字段
        self.assertTrue(response.success)
        self.assertEqual(response.data, {"id": 401})

    def test_add_user_score_data_missing_field(self):
        """测试添加分数数据时缺少必需字段。"""
        score_data = {'user_id': 1, 'score': 100}
        response = db_services.add_user_score_data(score_data)
        self.assertFalse(response.success)
        self.assertIn('title 不能为空', response.msg)
        mock_conn.insert.assert_not_called()

    def test_get_user_score_data_by_id_success(self):
        """测试通过ID成功获取分数数据。"""
        data_id = 401
        expected_data = {'id': data_id, 'user_id': 1, 'title': 'Day 1 Score'}
        mock_conn.fetch_rows.return_value = [expected_data]
        response = db_services.get_user_score_data_by_id(data_id)
        mock_conn.fetch_rows.assert_called_once_with(
            'user_date', condition={'id': data_id}
        )
        self.assertTrue(response.success)
        self.assertEqual(response.data, expected_data)

    def test_update_user_score_data_success(self):
        """测试成功更新分数数据。"""
        data_id = 401
        update_data = {'title': 'Day 1 Final Score', 'score': 110}
        mock_conn.update.return_value = 1 # 影响1行

        response = db_services.update_user_score_data(data_id, update_data.copy())

        mock_conn.update.assert_called_once()
        call_args = mock_conn.update.call_args[0][1]
        call_kwargs = mock_conn.update.call_args[1]
        self.assertIn('update_time', call_args)
        self.assertEqual(call_args['title'], 'Day 1 Final Score')
        self.assertNotIn('user_id', call_args)
        self.assertEqual(call_kwargs['condition'], {'id': data_id})
        self.assertTrue(response.success)

    def test_delete_user_score_data_by_id_success(self):
        """测试物理删除分数数据成功。"""
        data_id = 401
        mock_conn.delete.return_value = 1 # 影响1行

        response = db_services.delete_user_score_data_by_id(data_id)

        mock_conn.delete.assert_called_once_with('user_date', condition={'id': data_id})
        self.assertTrue(response.success)
        self.assertEqual(response.msg, "用户分数数据删除成功")

    def test_get_score_data_for_user(self):
        """测试获取指定用户的分数数据。"""
        user_id = 1
        expected_data = [{'id': 401, 'user_id': 1, 'title': 'Day 1 Score'}]
        mock_conn.fetch_rows.return_value = expected_data
        response = db_services.get_score_data_for_user(user_id)
        mock_conn.fetch_rows.assert_called_once_with(
             'user_date', condition={'user_id': user_id}
        )
        self.assertTrue(response.success)
        self.assertEqual(response.data, expected_data)

if __name__ == '__main__':
    unittest.main() 