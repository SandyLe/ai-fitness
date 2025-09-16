#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fitenss_items 
@File    ：result_type.py
@IDE     ：PyCharm 
@Author  ：写BUG的Botter
@Date    ：2025/4/11 09:30 
'''
import json
from decimal import Decimal

import json
from typing import Any, Union, Dict, List

def deep_remove_none(obj: Any) -> Any:
    """递归移除所有None值（支持嵌套字典/列表）"""
    if isinstance(obj, dict):
        return {k: deep_remove_none(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [deep_remove_none(elem) for elem in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

class Response:
    def __init__(self, code: int, msg: str, data: Union[Dict, List, None], success: bool):
        """初始化响应对象（自动深度清理data中的None值）。"""
        self.code = code
        self.msg = msg
        self.data = deep_remove_none(data)
        self.success = success

    @staticmethod
    def success(data: Union[Dict, List, None] = None, msg: str = "成功"):
        """成功响应（最终结果会清理None值）"""
        return Response(
            code=200,
            msg=msg,
            data=data,
            success=True
        )

    @staticmethod
    def fail(code: int, msg: str, data: Union[Dict, List, None] = None):
        """失败响应（最终结果会清理None值）"""
        return Response(
            code=code,
            msg=msg,
            data=data,
            success=False
        )

    def to_dict(self) -> dict:
        """转换为字典（data中已清理None值）"""
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data,
            "success": self.success
        }

    def to_json(self, indent: int = 2, sort_keys: bool = True) -> str:
        """生成美化JSON（自动处理None值）"""
        return json.dumps(
            self.to_dict(),
            indent=indent,
            sort_keys=sort_keys,
            ensure_ascii=False
        )

    def __str__(self) -> str:
        return self.to_json()