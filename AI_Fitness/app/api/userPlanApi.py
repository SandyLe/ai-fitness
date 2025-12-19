from flask import Blueprint, request, jsonify, render_template, session
from app import app
from app.services.db_services import user_plan, user_plan_detail, plan_detail_course

# 创建蓝图
user_plan_bp = Blueprint('user-plan', __name__)
@user_plan_bp.route("/get-user-plan-active", methods=["GET"])
def get_user_plan_active():
    try:
        user_id = session.get('user_id', '0')
        if user_id == '0':
            return jsonify({"success": False, 'error': "您还未登录，请登录后使用！！"})
        parent = user_plan.get_active_plan_for_user(user_id)
        details = user_plan_detail.get_plan_detail_by_plan_id(parent.data[0]['id'])
        if (details.data):
            details = [dict(i) for i in details.data]
        else:
            details = []
        return jsonify({"success": True, "data": {"plan": parent.data[0], "detailList": details}})
    except Exception as e:
        # 返回失败响应
        return jsonify({"success": False, "error": str(e)})

@user_plan_bp.route("/get-user-plan", methods=["GET"])
def get_user_plan():
    try:
        user_id = session.get('user_id', '0')
        if user_id == '0':
            return jsonify({"success": False, 'error': "您还未登录，请登录后使用！！"})
        plans = user_plan.get_no_active_plan_for_user(user_id)
        return jsonify({"success": True, "data": plans.data})
    except Exception as e:
        # 返回失败响应
        return jsonify({"success": False, "error": str(e)})

@user_plan_bp.route("/change-user-plan", methods=["POST"])
def change_user_plan():
    try:
        user_id = session.get('user_id', '0')
        params = request.get_json()
        origin_id = params['origin_id']
        new_id = params['new_id']
        user_plan.update_plan(origin_id, {'is_deleted':'0'})
        user_plan.update_plan(new_id, {'is_deleted':'2'})

        return get_user_plan_active()
    except Exception as e:
        # 返回失败响应
        return jsonify({"success": False, "error": str(e)})

@user_plan_bp.route("/save-plan-detail-course", methods=["POST"])
def save_plan_detail_course():
    try:
        user_id = session.get('user_id', '0')
        params = request.get_json()
        plan_dtl_id = params['plan_dtl_id']
        course_id = params['course_id']
        plan_dtl_course_id = params['plan_dtl_course_id']
        plan_detail_course_data = {'plan_dtl_course_id': plan_dtl_course_id, 'course_id': course_id, 'plan_dtl_id':plan_dtl_id}
        if (plan_dtl_course_id) :
            plan_detail_course.update_plan_detail_course(plan_dtl_course_id, plan_detail_course_data)
        else:
            result = plan_detail_course.add_plan_detail_course(plan_detail_course_data)
            plan_dtl_course_id = result.data['plan_dtl_course_id']

        return plan_dtl_course_id
    except Exception as e:
        # 返回失败响应
        return jsonify({"success": False, "error": str(e)})
