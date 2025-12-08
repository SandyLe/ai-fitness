'''
@input theme string 科室
@input gender string 性别
@input course string 部位
@return current_data json 当前数据
'''
import json
import os
import logging as python_logging

# 获取日志记录器
logger = python_logging.getLogger(__name__)

def get_current_data(theme, gender, course):
    # 科室称映射（常见名称 -> 医学名称）
    theme_mapping = {
        "Surgery": "Surgery", #外科
        "Chest": "Pectoralis",
        "Shoulders": "Deltoid",
        "Biceps": "Biceps",
        "Triceps": "Triceps",
        "Forearms": "Forearm",
        "Abdominals": "Abdominal",
        "Flanks": "Oblique",
        "Quads": "Quadriceps",
        "Calves": "Gastrocnemius",  # 可能需要检查实际文件名
        "Traps": "Trapezius",
        "Traps_middle": "Trapezius",  # 中部斜方肌也使用同一个文件
        "Lats": "Latissimus_dorsi",
        "Lowerback": "Erector_Spinae",
        "Glutes": "Gluteus",
        "Hamstrings": "Hamstrings"
    }
    
    # 将常见名称映射到解剖学名称
    medical_theme = theme_mapping.get(theme, theme)
    
    # 初始化返回数据
    current_data = {}
    
    try:
        # 检查文件是否存在
        json_path = f"app/config/fitness/{medical_theme}.json"
        if not os.path.exists(json_path):
            logger.error(f"找不到科室配置文件: {json_path}，原始科室名称: {theme}")
            # 返回默认数据
            return {
                'name': f'未知科室: {theme}',
                'course': {
                    'action': '暂无动作',
                    'video_src': '',
                    'Action_points': ['暂无动作要点']
                }
            }
        
        # 加载科室数据
        data = json.load(open(json_path, encoding="utf-8"))
        
        # 检查科室数据是否存在
        if medical_theme not in data:
            logger.error(f"科室配置文件中找不到科室数据: {medical_theme}")
            return {
                'name': f'配置错误: {theme}',
                'course': {
                    'action': '暂无动作',
                    'video_src': '',
                    'Action_points': ['配置文件中找不到该科室数据']
                }
            }
        
        # 设置科室名称
        current_data['name'] = data[medical_theme]['name']
        
        # 将部位名称首字母大写，以匹配配置文件中的格式
        course_key = course.capitalize()
        
        # 检查器材数据是否存在
        if course_key not in data[medical_theme]:
            logger.error(f"科室 {medical_theme} 不支持部位: {course_key}")
            # 尝试使用默认器材
            default_keys = [k for k in data[medical_theme].keys() if k not in ['comment', 'name']]
            if default_keys:
                course_key = default_keys[0]
                logger.info(f"使用默认部位: {course_key}")
            else:
                return {
                    'name': current_data['name'],
                    'course': {
                        'action': '暂无动作',
                        'video_src': '',
                        'Action_points': [f'该部门不支持部位: {course}']
                    }
                }
        
        # 获取器材数据
        course_data = data[medical_theme][course_key]
        
        # 检查视频源是否存在
        if 'video_src' not in course_data:
            logger.error(f"器材 {course_key} 缺少视频源配置")
            course_data['video_src'] = ''
        elif isinstance(course_data['video_src'], dict):
            # 根据性别选择视频
            if gender == 'man' and 'man' in course_data['video_src']:
                course_data['video_src'] = course_data['video_src']['man']
            elif gender == 'woman' and 'woman' in course_data['video_src']:
                course_data['video_src'] = course_data['video_src']['woman']
            else:
                # 如果没有对应性别的视频，使用任一可用视频
                video_src = course_data['video_src'].get('man', '')
                if not video_src:
                    video_src = course_data['video_src'].get('woman', '')
                course_data['video_src'] = video_src
        
        # 确保存在动作要点
        if 'Action_points' not in course_data or not course_data['Action_points']:
            course_data['Action_points'] = ['暂无动作要点']
        
        # 确保存在动作名称
        if 'action' not in course_data or not course_data['action']:
            course_data['action'] = '未命名动作'
        
        # 设置器材数据
        current_data['course'] = course_data

        # 肌肉描述description数据
        if 'description' in data[medical_theme]:
            current_data['description'] = data[medical_theme]['description']
        
        return current_data
        
    except Exception as e:
        logger.error(f"处理康训数据时出错: {str(e)}")
        return {
            'name': f'错误: {theme}',
            'course': {
                'action': '数据加载错误',
                'video_src': '',
                'Action_points': [f'加载数据时出错: {str(e)}']
            }
        }