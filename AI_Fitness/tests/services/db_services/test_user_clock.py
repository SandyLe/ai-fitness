#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

from app.services import db_services
from app.utils.result_type import Response

mock_conn = MagicMock()

@patch('app.services.db_services.user_clock.conn', mock_conn)
class TestUserClockService(unittest.TestCase):

    def setUp(self):
        mock_conn.reset_mock()

    def test_add_clock_in_success(self):
        """测试成功添加打卡记录。"""
        clock_time = datetime.now()
        clock_data = {'user_id': 1, 'data': clock_time}
        mock_conn.insert.return_value = 701 # 模拟插入ID

        response = db_services.add_clock_in(clock_data)

        mock_conn.insert.assert_called_once()
        call_args = mock_conn.insert.call_args[0][1]
        self.assertEqual(call_args['user_id'], 1)
        self.assertEqual(call_args['data'], clock_time)
        self.assertIn('created_time', call_args)
        self.assertIn('update_time', call_args)
        # self.assertNotIn('is_deleted', call_args) # 无 is_deleted 字段
        self.assertTrue(response.success)
        self.assertEqual(response.data, {"id": 701})

    def test_add_clock_in_missing_field(self):
        """测试添加打卡记录时缺少必需字段 'data'。"""
        clock_data = {'user_id': 1}
        response = db_services.add_clock_in(clock_data)
        self.assertFalse(response.success)
        self.assertIn('data 不能为空', response.msg)
        mock_conn.insert.assert_not_called()

    def test_get_clock_in_by_id_success(self):
        """测试通过ID成功获取打卡记录。"""
        clock_id = 701
        clock_time = datetime.now()
        expected_data = {'id': clock_id, 'user_id': 1, 'data': clock_time}
        mock_conn.fetch_rows.return_value = [expected_data]
        response = db_services.get_clock_in_by_id(clock_id)
        mock_conn.fetch_rows.assert_called_once_with(
            'user_clock', condition={'id': clock_id}
        )
        self.assertTrue(response.success)
        self.assertEqual(response.data, expected_data)
        # 可选检查：如果实现中重命名了 'data' 字段，在响应中进行检查
        # self.assertIn('clock_time', response.data)
        # self.assertNotIn('data', response.data)

    def test_delete_clock_in_by_id_success(self):
        """测试物理删除打卡记录成功。"""
        clock_id = 701
        mock_conn.delete.return_value = 1 # 影响1行

        response = db_services.delete_clock_in_by_id(clock_id)

        mock_conn.delete.assert_called_once_with('user_clock', condition={'id': clock_id})
        self.assertTrue(response.success)
        self.assertEqual(response.msg, "打卡记录删除成功")

    def test_get_clock_ins_for_user(self):
        """测试获取指定用户的打卡记录。"""
        user_id = 1
        clock_time = datetime.now()
        expected_data = [{'id': 701, 'user_id': 1, 'data': clock_time}]
        mock_conn.fetch_rows.return_value = expected_data
        response = db_services.get_clock_ins_for_user(user_id)
        mock_conn.fetch_rows.assert_called_once_with(
             'user_clock', condition={'user_id': user_id}
             # 如果实现了日期范围条件并且需要测试，在此添加检查
        )
        self.assertTrue(response.success)
        self.assertEqual(response.data, expected_data)

if __name__ == '__main__':
    unittest.main() 