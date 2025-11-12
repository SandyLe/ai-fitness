import unittest
from app.services.db_services.user_discussion import (add_discussion , update_discussion , delete_discussion ,
                                                      get_discussion , get_discussion_exist)

from datetime import datetime
class MyTestCase(unittest.TestCase):
    def test_add_discussion(self):
        add_discussion({
            "title": "如何康训",
            "content": "1.坚持打卡 ， 2.坚持锻炼",
            "image_path": "https://123.png",
            "created_by": None,
            "created_time": datetime.now(),
            "update_by": None,
            "update_time": datetime.now(),
        })
    def test_update_discussion(self):
        update_discussion({
            "title": "如何康训",
            "content": "1.坚持打卡 ， 2.坚持锻炼",
            "image_path": "https://123.png",
            "created_by": "test_unit",
            "created_time": datetime.now(),
            "update_by": 'admin',
            "update_time": datetime.now(),
        } , {'id' : 1})
    def test_delete_discussion(self):
        delete_discussion({
            "id" : 1 ,
        })
    def test_get_discussion(self):
        get_discussion({
            "id" : 2 ,
        })
    def test_get_discussion_exist(self):
        get_discussion_exist({
            "id" : 2 ,
        })

if __name__ == '__main__':
    unittest.main()
