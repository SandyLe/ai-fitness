from datetime import datetime
import logging as python_logging
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.services import db_service
from app.services.db_services import user_clock
from app.services.basefunc import get_current_data
from functools import wraps
from app.utils.login_required import login_required
import json
import os
import random
import time
# from app.utils import login_required

# 创建蓝图
clock_bp = Blueprint('clock', __name__, url_prefix='/clock')

# 配置日志
python_logging.basicConfig(
    level=python_logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = python_logging.getLogger(__name__)

# 开始训练
@clock_bp.route('/add_clock_in', methods=['GET', 'POST'])
# @login_required
def add_clock_in():
    # 从session获取用户ID
    user_clock_data = request.get_json()
    # user_clock_data = json.loads(data)
    user_id = session.get('user_id', '0')
    logger.info(f"user_id>>>={user_id}")
    user_clock_data['data'] = datetime.now()
    user_clock_data['created_by'] = user_id
    user_clock_data['update_by'] = user_id
    result = user_clock.add_clock_in(user_clock_data)

    if (result.code == 500):
        logger.error(result.data)

    return jsonify(result.__dict__)


@clock_bp.route('/get_clock_ins_for_user_date', methods=['GET'])
def get_clock_ins_for_user_date():
    """获取当前登录用户的ID"""
    user_id = session.get('user_id', '7')
    result_clock = user_clock.count_clock_in(user_id, datetime.now().timestamp(), datetime.now().timestamp())
    return jsonify(result_clock.__dict__)
'''
肌肉练习
muscle:肌肉名称
gender:性别
equipment:器材
'''
@clock_bp.route('/<muscle>/<gender>/<equipment>', methods=['GET', 'POST'])
# @login_required
def fitness_muscle(muscle, gender, equipment):
    try:
        # 从session获取用户ID
        user_id = session.get('user_id', '0')
        
        # 记录请求信息
        logger.info(f"康训请求: 肌肉={muscle}, 性别={gender}, 器材={equipment}, 用户ID={user_id}")
        
        # 验证性别参数
        if gender not in ['man', 'woman']:
            logger.warning(f"无效的性别参数: {gender}，使用默认值 'man'")
            gender = 'man'
        
        # 验证器材参数
        valid_equipment = ['dumbbell', 'bodyweight']
        if equipment not in valid_equipment:
            logger.warning(f"无效的器材参数: {equipment}，使用默认值 'dumbbell'")
            equipment = 'dumbbell'
        
        # 获取用户数据
        user = ''
        
        # 获取当前数据
        current_data = get_current_data(muscle, gender, equipment)
        
        return render_template('fitness/main_fitness.html', user=user, id=user_id, current_data=current_data)
    
    except Exception as e:
        # 记录错误
        logger.error(f"处理康训请求时出错: {str(e)}")
        
        # 返回错误页面或重定向到开始页面
        flash(f"加载康训内容时出错: {str(e)}", "error")
        return redirect(url_for('fitness.start_fitness'))


@clock_bp.route('/get_report', methods=['GET'])
def get_fitness_report():
    """获取康训报告数据"""
    try:
        # 获取请求参数
        muscle = request.args.get('muscle', 'trapezius')
        exercise = request.args.get('exercise', '哑铃划船')
        
        logger.info(f"收到康训报告请求: 肌肉={muscle}, 动作={exercise}")
        
        # 添加延迟，模拟报告生成过程
        time.sleep(1)  # 延迟1秒，与前端的延迟一起，总共约3-4秒的加载时间
        
        # 构建报告文件路径
        report_file = f"{muscle}_report.json"
        report_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'datajson', report_file)
        
        # 检查文件是否存在
        if not os.path.exists(report_path):
            logger.error(f"报告文件不存在: {report_path}")
            return jsonify({
                "error": "报告数据不可用", 
                "score": 80,
                "summary": "无法获取详细报告，这是一个默认生成的报告。",
                "issues": [{"title": "数据缺失", "description": "未能找到对应的报告数据文件。"}],
                "suggestions": ["请尝试其他训练动作"]
            }), 200  # 返回200而不是404，避免前端报错
        
        # 读取报告数据
        with open(report_path, 'r', encoding='utf-8') as f:
            report_data = json.load(f)
            logger.info(f"成功读取报告文件: {report_file}")
        
        # 检查动作是否匹配
        if report_data.get('action', '') != exercise and not exercise.startswith(report_data.get('action', '')):
            logger.warning(f"请求的动作 '{exercise}' 与报告中的动作 '{report_data.get('action', '')}' 不完全匹配，但仍继续使用")
        
        # 从报告中随机选择一条
        reports = report_data.get('reports', [])
        if not reports:
            logger.warning(f"报告文件 {report_file} 中没有可用的报告数据")
            return jsonify({
                "error": "没有可用的报告数据",
                "score": 75,
                "summary": "无法获取详细报告，这是一个默认生成的报告。",
                "issues": [{"title": "数据缺失", "description": "报告文件中没有可用的报告数据。"}],
                "suggestions": ["请尝试其他训练动作"]
            }), 200
        
        # 随机选择一条报告
        selected_report = random.choice(reports)
        
        # 确保报告包含所有必要字段
        if 'score' not in selected_report:
            selected_report['score'] = 85
        if 'summary' not in selected_report:
            selected_report['summary'] = f"您的{exercise}动作整体表现良好。"
        if 'issues' not in selected_report:
            selected_report['issues'] = [{"title": "数据不完整", "description": "无法提供详细的动作分析。"}]
        if 'suggestions' not in selected_report:
            selected_report['suggestions'] = ["保持良好的训练习惯", "注意动作的标准性"]
        
        # 添加日志
        logger.info(f"成功获取康训报告: 肌肉={muscle}, 动作={exercise}, 评分={selected_report.get('score', 'N/A')}")
        
        # 返回前检查数据完整性
        logger.debug(f"返回报告数据: {json.dumps(selected_report, ensure_ascii=False)[:100]}...")
        
        return jsonify(selected_report)
    
    except json.JSONDecodeError as je:
        logger.exception(f"解析报告JSON数据时出错: {str(je)}")
        return jsonify({
            "error": "报告数据格式错误",
            "score": 70,
            "summary": "无法解析报告数据，这是一个默认生成的报告。",
            "issues": [{"title": "数据格式错误", "description": "报告文件格式不正确。"}],
            "suggestions": ["请联系管理员修复数据问题"]
        }), 200
    
    except Exception as e:
        logger.exception(f"获取康训报告时出错: {str(e)}")
        return jsonify({
            "error": "获取报告数据失败", 
            "message": str(e),
            "score": 65,
            "summary": "生成报告时发生错误，这是一个默认生成的报告。",
            "issues": [{"title": "系统错误", "description": f"错误信息: {str(e)}"}],
            "suggestions": ["请稍后再试", "如果问题持续存在，请联系管理员"]
        }), 200  # 返回200而不是500，避免前端报错

@clock_bp.route('/pose_detection', methods=['GET', 'POST'])
def pose_detection():
    if request.method == 'GET':
        # 从session获取用户ID
        return render_template('fitness/pose_detection.html')


# 在现有导入语句下添加
from app.services.db_services.user_date import save_fitness_report

# 在现有路由下添加
@clock_bp.route('/save_report', methods=['POST'])
def save_fitness_report_route():
    """保存康训报告数据到数据库"""
    try:
        # 获取请求数据
        data = request.json
        
        if not data:
            return jsonify({"success": False, "msg": "请求数据为空"}), 400
        
        # 提取必要参数
        user_id = data.get('user_id')
        exercise_type = data.get('exercise_type')
        report_data = data.get('report_data')
        action_analyse = data.get('action_analyse', '')  # 获取动作分析字段
        
        # 添加组数和次数到报告数据
        if report_data:
            report_data['group'] = data.get('group', 1)
            report_data['reps'] = data.get('reps', 10)
            report_data['action_analyse'] = action_analyse  # 添加动作分析到报告数据
        
        # 验证必要参数
        if not user_id:
            return jsonify({"success": False, "msg": "用户ID不能为空"}), 400
        
        if not exercise_type:
            return jsonify({"success": False, "msg": "训练动作不能为空"}), 400
            
        if not report_data:
            return jsonify({"success": False, "msg": "报告数据不能为空"}), 400
        
        # 调用服务保存报告
        result = save_fitness_report(user_id, report_data, exercise_type, action_analyse)
        
        if result.success:
            return jsonify({"success": True, "msg": "报告保存成功", "data": result.data}), 200
        else:
            return jsonify({"success": False, "msg": result.msg}), 400
            
    except Exception as e:
        logger.exception(f"保存康训报告时出错: {str(e)}")
        return jsonify({"success": False, "msg": f"保存报告失败: {str(e)}"}), 500


# 添加获取当前用户ID的路由