'''
@input muscle string 肌肉名称
@input gender string 性别
@input equipment string 器材
@return current_data json 当前数据
'''
import json
import os
import logging as python_logging

# 获取日志记录器
logger = python_logging.getLogger(__name__)

def get_current_data(muscle, gender, equipment):
    # 肌肉名称映射（常见名称 -> 解剖学名称）
    muscle_mapping = {
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
    anatomical_muscle = muscle_mapping.get(muscle, muscle)
    
    # 初始化返回数据
    current_data = {}
    
    try:
        # 检查文件是否存在
        json_path = f"app/config/fitness/{anatomical_muscle}.json"
        if not os.path.exists(json_path):
            logger.error(f"找不到肌肉配置文件: {json_path}，原始肌肉名称: {muscle}")
            # 返回默认数据
            return {
                'name': f'未知肌肉: {muscle}',
                'equipment': {
                    'action': '暂无动作',
                    'video_src': '',
                    'Action_points': ['暂无动作要点']
                }
            }
        
        # 加载肌肉数据
        data = json.load(open(json_path, encoding="utf-8"))
        
        # 检查肌肉数据是否存在
        if anatomical_muscle not in data:
            logger.error(f"肌肉配置文件中找不到肌肉数据: {anatomical_muscle}")
            return {
                'name': f'配置错误: {muscle}',
                'equipment': {
                    'action': '暂无动作',
                    'video_src': '',
                    'Action_points': ['配置文件中找不到该肌肉数据']
                }
            }
        
        # 设置肌肉名称
        current_data['name'] = data[anatomical_muscle]['name']
        
        # 将器材名称首字母大写，以匹配配置文件中的格式
        equipment_key = equipment.capitalize()
        
        # 检查器材数据是否存在
        if equipment_key not in data[anatomical_muscle]:
            logger.error(f"肌肉 {anatomical_muscle} 不支持器材: {equipment_key}")
            # 尝试使用默认器材
            default_keys = [k for k in data[anatomical_muscle].keys() if k not in ['comment', 'name']]
            if default_keys:
                equipment_key = default_keys[0]
                logger.info(f"使用默认器材: {equipment_key}")
            else:
                return {
                    'name': current_data['name'],
                    'equipment': {
                        'action': '暂无动作',
                        'video_src': '',
                        'Action_points': [f'该肌肉不支持器材: {equipment}']
                    }
                }
        
        # 获取器材数据
        equipment_data = data[anatomical_muscle][equipment_key]
        
        # 检查视频源是否存在
        if 'video_src' not in equipment_data:
            logger.error(f"器材 {equipment_key} 缺少视频源配置")
            equipment_data['video_src'] = ''
        elif isinstance(equipment_data['video_src'], dict):
            # 根据性别选择视频
            if gender == 'man' and 'man' in equipment_data['video_src']:
                equipment_data['video_src'] = equipment_data['video_src']['man']
            elif gender == 'woman' and 'woman' in equipment_data['video_src']:
                equipment_data['video_src'] = equipment_data['video_src']['woman']
            else:
                # 如果没有对应性别的视频，使用任一可用视频
                video_src = equipment_data['video_src'].get('man', '')
                if not video_src:
                    video_src = equipment_data['video_src'].get('woman', '')
                equipment_data['video_src'] = video_src
        
        # 确保存在动作要点
        if 'Action_points' not in equipment_data or not equipment_data['Action_points']:
            equipment_data['Action_points'] = ['暂无动作要点']
        
        # 确保存在动作名称
        if 'action' not in equipment_data or not equipment_data['action']:
            equipment_data['action'] = '未命名动作'
        
        # 设置器材数据
        current_data['equipment'] = equipment_data

        # 肌肉描述description数据
        if 'description' in data[anatomical_muscle]:
            current_data['description'] = data[anatomical_muscle]['description']
        
        return current_data
        
    except Exception as e:
        logger.error(f"处理健身数据时出错: {str(e)}")
        return {
            'name': f'错误: {muscle}',
            'equipment': {
                'action': '数据加载错误',
                'video_src': '',
                'Action_points': [f'加载数据时出错: {str(e)}']
            }
        }