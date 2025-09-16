#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from unittest.mock import patch, MagicMock

from app.services import db_services
from app.utils.result_type import Response

mock_conn = MagicMock()

# 通过 __init__.py 中定义的别名进行测试
@patch('app.services.db_services.user_plan_date_mapping.conn', mock_conn)
class TestUserPlanDateMappingService(unittest.TestCase):

    def setUp(self):
        mock_conn.reset_mock()

    def test_add_plan_date_mapping_success(self):
        """测试成功添加计划-数据映射关系。"""
        mapping_data = {'data_id': 401, 'plan_id': 301} # user_date.id, user_plan.id
        mock_conn.count.return_value = 0 # 模拟映射不存在
        mock_conn.insert.return_value = 801 # 模拟插入ID

        response = db_services.add_plan_date_mapping(mapping_data)

        mock_conn.count.assert_called_once_with(
            'user_plan_date_mapping', condition={'data_id': 401, 'plan_id': 301}
        )
        mock_conn.insert.assert_called_once()
        call_args = mock_conn.insert.call_args[0][1]
        self.assertIn('created_time', call_args)
        self.assertIn('update_time', call_args)
        # self.assertNotIn('is_deleted', call_args) # 无 is_deleted 字段
        self.assertTrue(response.success)
        self.assertEqual(response.data, {"id": 801})

    def test_add_plan_date_mapping_exists(self):
        """测试添加已存在的映射关系。"""
        mapping_data = {'data_id': 401, 'plan_id': 301}
        mock_conn.count.return_value = 1 # 模拟映射已存在

        response = db_services.add_plan_date_mapping(mapping_data)

        mock_conn.count.assert_called_once()
        mock_conn.insert.assert_not_called()
        self.assertFalse(response.success)
        self.assertEqual(response.code, 409)

    def test_delete_plan_date_mapping_by_id_success(self):
        """测试使用别名物理删除映射关系成功。"""
        mapping_id = 801
        mock_conn.delete.return_value = 1 # 影响1行

        # 使用删除函数的别名
        response = db_services.delete_plan_date_mapping_by_id(mapping_id)

        mock_conn.delete.assert_called_once_with('user_plan_date_mapping', condition={'id': mapping_id})
        self.assertTrue(response.success)
        self.assertEqual(response.msg, "映射关系删除成功")

    def test_check_plan_date_mapping_exists_true(self):
        """测试使用别名检查映射关系是否存在 (True 情况)。"""
        data_id = 401
        plan_id = 301
        mock_conn.count.return_value = 1
        # 使用检查函数的别名
        response = db_services.check_plan_date_mapping_exists(data_id, plan_id)
        mock_conn.count.assert_called_once_with(
            'user_plan_date_mapping', condition={'data_id': data_id, 'plan_id': plan_id}
        )
        self.assertTrue(response.success)
        self.assertTrue(response.data)

    def test_get_plans_for_data(self):
        """测试获取指定数据ID关联的所有计划ID。"""
        data_id = 401
        expected_ids = [301, 305]
        mock_conn.fetch_rows.return_value = [{'plan_id': 301}, {'plan_id': 305}]

        response = db_services.get_plans_for_data(data_id)

        mock_conn.fetch_rows.assert_called_once_with(
            'user_plan_date_mapping', condition={'data_id': data_id}, fields=['plan_id']
        )
        self.assertTrue(response.success)
        self.assertEqual(response.data, expected_ids)

    def test_get_data_for_plan(self):
        """测试获取指定计划ID关联的所有数据ID。"""
        plan_id = 301
        expected_ids = [401, 402]
        mock_conn.fetch_rows.return_value = [{'data_id': 401}, {'data_id': 402}]

        response = db_services.get_data_for_plan(plan_id)

        mock_conn.fetch_rows.assert_called_once_with(
            'user_plan_date_mapping', condition={'plan_id': plan_id}, fields=['data_id']
        )
        self.assertTrue(response.success)
        self.assertEqual(response.data, expected_ids)

if __name__ == '__main__':
    unittest.main() 