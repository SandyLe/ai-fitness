#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from unittest.mock import patch, MagicMock

from app.services import db_services
from app.utils.result_type import Response

mock_conn = MagicMock()

@patch('app.services.db_services.user_plan.conn', mock_conn)
class TestUserPlanService(unittest.TestCase):

    def setUp(self):
        mock_conn.reset_mock()

    def test_add_plan_success(self):
        """测试成功添加用户计划。"""
        plan_data = {'user_id': 1, 'plan': 'Run 5k', 'context': 'Morning run'}
        mock_conn.insert.return_value = 301 # 模拟插入ID

        response = db_services.add_plan(plan_data)

        mock_conn.insert.assert_called_once()
        call_args = mock_conn.insert.call_args[0][1]
        self.assertEqual(call_args['plan'], 'Run 5k')
        self.assertIn('created_time', call_args)
        self.assertIn('update_time', call_args)
        self.assertEqual(call_args.get('is_deleted'), 0)
        self.assertTrue(response.success)
        self.assertEqual(response.data, {"id": 301})

    def test_add_plan_missing_field(self):
        """测试添加计划时缺少必需字段。"""
        plan_data = {'user_id': 1, 'context': 'Morning run'}
        response = db_services.add_plan(plan_data)
        self.assertFalse(response.success)
        self.assertIn('plan 不能为空', response.msg)
        mock_conn.insert.assert_not_called()

    def test_get_plan_by_id_success(self):
        """测试通过ID成功获取计划。"""
        plan_id = 301
        expected_data = {'id': plan_id, 'user_id': 1, 'plan': 'Run 5k', 'is_deleted': 0}
        mock_conn.fetch_rows.return_value = [expected_data]
        response = db_services.get_plan_by_id(plan_id)
        mock_conn.fetch_rows.assert_called_once_with(
            'user_plan', condition={'id': plan_id, 'is_deleted': 0}
        )
        self.assertTrue(response.success)
        self.assertEqual(response.data, expected_data)

    def test_update_plan_success(self):
        """测试成功更新计划。"""
        plan_id = 301
        update_data = {'plan': 'Run 10k', 'context': 'Evening run'}
        mock_conn.update.return_value = 1 # 影响1行

        response = db_services.update_plan(plan_id, update_data.copy())

        mock_conn.update.assert_called_once()
        call_args = mock_conn.update.call_args[0][1]
        call_kwargs = mock_conn.update.call_args[1]
        self.assertIn('update_time', call_args)
        self.assertEqual(call_args['plan'], 'Run 10k')
        self.assertNotIn('user_id', call_args)
        self.assertEqual(call_kwargs['condition'], {'id': plan_id, 'is_deleted': 0})
        self.assertTrue(response.success)

    def test_delete_plan_by_id_success(self):
        """测试逻辑删除计划成功。"""
        plan_id = 301
        mock_conn.update.return_value = 1 # 影响1行

        response = db_services.delete_plan_by_id(plan_id)

        mock_conn.update.assert_called_once()
        call_args = mock_conn.update.call_args[0][1]
        call_kwargs = mock_conn.update.call_args[1]
        self.assertEqual(call_args.get('is_deleted'), 1)
        self.assertIn('update_time', call_args)
        self.assertEqual(call_kwargs['condition'], {'id': plan_id})
        self.assertTrue(response.success)

    def test_get_plans_for_user(self):
        """测试获取指定用户的所有计划。"""
        user_id = 1
        expected_plans = [{'id': 301, 'user_id': 1, 'plan': 'Run 5k'}]
        mock_conn.fetch_rows.return_value = expected_plans
        response = db_services.get_plans_for_user(user_id)
        mock_conn.fetch_rows.assert_called_once_with(
             'user_plan', condition={'user_id': user_id, 'is_deleted': 0}
        )
        self.assertTrue(response.success)
        self.assertEqual(response.data, expected_plans)

if __name__ == '__main__':
    unittest.main() 