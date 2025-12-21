import datetime

from flask import Blueprint, request, jsonify, render_template, session
from app import app
from app.services.db_services import course, course_training_record

# 创建蓝图
course_bp = Blueprint('course', __name__, url_prefix='/course')
@course_bp.route("/save_course_training_record", methods=["POST"])
def save_course_training_record():
    try:
        user_id = session.get('user_id', '0')
        training_records = request.get_json()
        i = 0
        ids = []
        for record in training_records:
            record['user_id'] = user_id
            record['start_time'] = datetime.datetime.fromtimestamp(record['start_time']/1000)
            record['end_time'] = datetime.datetime.fromtimestamp(record['end_time']/1000)
            result = course_training_record.add_training_record(record).data
            ids.append(result['result_id'])
            i = i + 1

        return jsonify({"success": True, "data": {"record_ids": ids}})
    except Exception as e:
        # 返回失败响应
        return jsonify({"success": False, "error": str(e)})

@course_bp.route("/get-courses", methods=["GET"])
def get_user_plan():
    try:
        user_id = session.get('user_id', '0')
        if user_id == '0':
            return jsonify({"success": False, 'error': "您还未登录，请登录后使用！！"})
        param = {'is_deleted': 0 }
        courses = course.get_course(param)
        return jsonify({"success": True, "data": courses.data})
    except Exception as e:
        # 返回失败响应
        return jsonify({"success": False, "error": str(e)})