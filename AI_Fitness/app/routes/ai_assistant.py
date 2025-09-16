from flask import Blueprint, request, jsonify, render_template, session
from app.services import db_service, ai_service

# 创建蓝图
ai_assistant_bp = Blueprint('ai_assistant', __name__, url_prefix='/ai_assistant')

# 智能助手页面路由
@ai_assistant_bp.route("/", methods=['GET', 'POST'])
def ai_assistant():
    # 从session获取用户ID，如果没有则默认为0
    user_id = session.get('user_id', '0')
    user = ''
    return render_template("ai_assistant/ai_assistant.html", id=user_id, user=user, active_page='ai_assistant')
