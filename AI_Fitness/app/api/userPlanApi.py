from flask import Blueprint, request, jsonify, render_template, session
from app import app
from app.services.db_services import user_plan, user_plan_detail

# 创建蓝图
user_plan_bp = Blueprint('user-plan', __name__)
@user_plan_bp.route("/get-user-plan", methods=["GET"])
def get_user_plan():
    try:
        user_id = session.get('user_id', '0')
        if user_id == '0':
            return jsonify({"success": False, 'error': "您还未登录，请登录后使用！！"})
        parent = user_plan.get_active_plan_for_user(user_id)
        details = user_plan_detail.get_plan_detail_by_plan_id(parent.data[0]['id'])
        details = [dict(i) for i in details.data]
        return jsonify({"success": True, "data": {"plan": parent.data[0], "detailList": details}})
    except Exception as e:
        # 返回失败响应
        return jsonify({"success": False, "error": str(e)})
