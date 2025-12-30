from datetime import datetime
import logging as python_logging
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.services.db_services import user_info, user_nutrition_guidance, user_nutrition_guidance_detail
from app.services import db_service
from app.services.basefunc import get_current_data
from functools import wraps
from app.utils.login_required import login_required
import json
import os
import random
import time
# from app.utils import login_required

# 创建蓝图
nutrition_bp = Blueprint('nutrition', __name__, url_prefix='/nutrition')

# 配置日志
python_logging.basicConfig(
    level=python_logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = python_logging.getLogger(__name__)

@nutrition_bp.route('/user_nutrition', methods=['GET', 'POST'])
def user_nutrition():
    # 获取用户ID
    user_id = session.get('user_id')
    if not user_id:
        flash('请先登录', 'error')
        return redirect(url_for('auth.login'))

    # 获取用户信息
    user_result = user_info.get_user_by_id(user_id)
    if not user_result.success:
        flash('获取用户信息失败', 'error')
        return redirect(url_for('auth.login'))

    user = user_result.data

    parent = user_nutrition_guidance.get_active_guidance_for_user(user_id)
    parent_data = {}
    details_nutrition = []
    details_food = []

    if (parent.data):
        parent_data = parent.data[0]
        details_nutrition = user_nutrition_guidance_detail.get_guidance_detail_by_guidance_id(parent_data['id'], 'T01')
        details_food = user_nutrition_guidance_detail.get_guidance_detail_by_guidance_id(parent_data['id'], 'T02')

    if request.method == 'GET':
        # 从session获取用户ID
        return render_template('nutrition/user_nutrition.html', user = user, guidance=parent_data, nutrition=details_nutrition, food = details_food)

