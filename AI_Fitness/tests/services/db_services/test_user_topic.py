#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from unittest.mock import patch, MagicMock

from app.services import db_services
from app.utils.result_type import Response

mock_conn = MagicMock()

@patch('app.services.db_services.user_topic.conn', mock_conn)
class TestUserTopicService(unittest.TestCase):

    def setUp(self):
        mock_conn.reset_mock()

    def test_add_topic_success(self):
        """测试添加顶层主题（parent_id为None）成功。"""
        # 使用 None 代表顶层主题
        topic_data = {'discussion_id': 10, 'parent_id': None, 'created_by': 1}
        mock_conn.insert.return_value = 201 # 模拟插入ID

        response = db_services.add_topic(topic_data)

        mock_conn.insert.assert_called_once()
        call_args = mock_conn.insert.call_args[0][1]
        self.assertEqual(call_args['discussion_id'], 10)
        self.assertIsNone(call_args['parent_id']) # 确认插入时 parent_id 是 None
        self.assertIn('created_time', call_args)
        self.assertIn('update_time', call_args)
        # self.assertNotIn('is_deleted', call_args) # 无 is_deleted 字段
        self.assertTrue(response.success)
        self.assertEqual(response.data, {"id": 201})

    def test_add_topic_missing_field(self):
        """测试添加主题时缺少 discussion_id。"""
        # parent_id 可以为 None
        topic_data = {'parent_id': None}
        response = db_services.add_topic(topic_data)
        self.assertFalse(response.success)
        self.assertIn('discussion_id 不能为空', response.msg)
        mock_conn.insert.assert_not_called()

    def test_get_topic_by_id_success(self):
        """测试通过ID获取顶层主题成功（预期结果不含parent_id）。"""
        topic_id = 201
        # 模拟数据库返回的数据（包含 parent_id: None）
        db_return_data = {'id': topic_id, 'discussion_id': 10, 'parent_id': None}
        # 预期最终 response.data 的结果（因为 deep_remove_none 会移除 parent_id）
        expected_response_data = {'id': topic_id, 'discussion_id': 10}

        mock_conn.fetch_rows.return_value = [db_return_data]
        response = db_services.get_topic_by_id(topic_id)
        mock_conn.fetch_rows.assert_called_once_with(
            'user_topic', condition={'id': topic_id}
        )
        self.assertTrue(response.success)
        # 调试：打印实际返回的数据
        print(f"\nDEBUG [test_get_topic_by_id_success] response.data: {response.data}\n")
        # 断言 response.data 不包含 parent_id
        self.assertEqual(response.data, expected_response_data)

    # 更新测试可能需要添加可更新的字段 (例如, 如果添加了 'content')
    # def test_update_topic_success(self): ...

    def test_delete_topic_by_id_success(self):
        """测试物理删除主题成功。"""
        topic_id = 201
        mock_conn.delete.return_value = 1 # 影响1行

        response = db_services.delete_topic_by_id(topic_id)

        mock_conn.delete.assert_called_once_with('user_topic', condition={'id': topic_id})
        self.assertTrue(response.success)
        self.assertEqual(response.msg, "回复删除成功")

    def test_delete_topic_by_id_not_found(self):
        """测试删除不存在的主题。"""
        topic_id = 999
        mock_conn.delete.return_value = 0 # 影响0行
        response = db_services.delete_topic_by_id(topic_id)
        mock_conn.delete.assert_called_once_with('user_topic', condition={'id': topic_id})
        self.assertFalse(response.success)
        self.assertEqual(response.code, 404)
        self.assertEqual(response.msg, "未找到要删除的回复")

    def test_get_topics_for_discussion_top_level(self):
        """测试获取指定论坛的顶级主题（预期结果不含parent_id）。"""
        discussion_id = 10
        # 模拟数据库返回的数据（包含 parent_id: None）
        db_return_topics = [{'id': 201, 'discussion_id': 10, 'parent_id': None}]
        # 预期最终 response.data 的结果列表（每个字典都不含 parent_id）
        expected_response_topics = [{'id': 201, 'discussion_id': 10}]

        # 在调用前直接设置模拟返回值
        mock_conn.fetch_rows.return_value = db_return_topics

        response = db_services.get_topics_for_discussion(discussion_id)

        # 检查 fetch_rows 是否以正确的条件被调用 (仅 discussion_id 和 parent_id: None)
        mock_conn.fetch_rows.assert_called_once_with(
            'user_topic', condition={'discussion_id': discussion_id, 'parent_id': None}
        )
        self.assertTrue(response.success)
        # 调试：打印实际返回的数据
        print(f"\nDEBUG [test_get_topics_for_discussion_top_level] response.data: {response.data}\n")
        # 断言 response.data 中的字典不包含 parent_id
        self.assertEqual(response.data, expected_response_topics)

    def test_get_topics_for_discussion_with_parent(self):
        """测试获取指定论坛和父主题下的子主题。"""
        discussion_id = 10
        parent_id = 201
        expected_topics = [{'id': 205, 'discussion_id': 10, 'parent_id': parent_id}]
        mock_conn.fetch_rows.return_value = expected_topics
        response = db_services.get_topics_for_discussion(discussion_id, parent_id=parent_id)
        mock_conn.fetch_rows.assert_called_once_with(
            'user_topic', condition={'discussion_id': discussion_id, 'parent_id': parent_id}
        )
        self.assertTrue(response.success)
        self.assertEqual(response.data, expected_topics)

if __name__ == '__main__':
    unittest.main() 