from flask import Blueprint, request, render_template, jsonify, session, redirect, url_for, flash
from app.services.db_services import user_discussion, user_topic, user_mapping
from datetime import datetime
import os
from werkzeug.utils import secure_filename

# 创建蓝图
community_bp = Blueprint('community', __name__, url_prefix='/community')

# 论坛首页
@community_bp.route('/', methods=['GET'])
def community():
    # 从session获取用户ID
    user_id = session.get('user_id', '0')
    
    # 获取所有未删除的讨论
    # 使用user_discussion模块获取讨论列表
    discussions_response = user_discussion.get_discussion({'is_deleted': 0})
    
    if discussions_response.success:
        discussions = discussions_response.data
        
        # 为每个讨论获取回复数量和作者名称
        for discussion in discussions:
            # 获取回复数量
            replies_response = user_topic.get_topics_for_discussion(discussion['id'])
            discussion['reply_count'] = len(replies_response.data) if replies_response.success else 0
            
            # 获取作者名称 (这里需要额外查询用户表，假设有一个获取用户信息的函数)
            # 由于没有提供用户服务模块，这里暂时使用created_by作为author_name
            discussion['author_name'] = discussion['created_by']
    else:
        discussions = []
    
    return render_template('community/community.html', discussions=discussions, id=user_id, active_page='community')

# 查看讨论详情
@community_bp.route('/discussion/<int:discussion_id>', methods=['GET'])
def view_discussion(discussion_id):
    user_id = session.get('user_id', '0')
    
    # 获取讨论详情
    discussion_response = user_discussion.get_discussion_by_id(discussion_id)
    
    if not discussion_response.success:
        flash('讨论不存在或已被删除', 'error')
        return redirect(url_for('community.community'))
    
    discussion = discussion_response.data
    # 获取作者名称 (同样，这里需要额外查询)
    discussion['author_name'] = discussion['created_by']
    
    # 获取讨论的回复
    replies_response = user_topic.get_topics_for_discussion(discussion_id)
    
    if replies_response.success:
        replies = replies_response.data
        # 为每个回复获取作者名称
        for reply in replies:
            reply['author_name'] = reply['created_by']
    else:
        replies = []
    
    return render_template('community/discussion.html', discussion=discussion, replies=replies, id=user_id, active_page='community')

# 创建新讨论
@community_bp.route('/create', methods=['GET', 'POST'])
def create_discussion():
    user_id = session.get('user_id')
    
    if not user_id:
        flash('请先登录', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image_path = ''
        
        # 处理图片上传
        if 'image' in request.files and request.files['image'].filename:
            image = request.files['image']
            filename = secure_filename(image.filename)
            # 确保目录存在
            upload_dir = os.path.join('app', 'static', 'uploads', 'community')
            os.makedirs(upload_dir, exist_ok=True)
            
            # 保存文件
            image_path = os.path.join('uploads', 'community', filename)
            image.save(os.path.join('app', 'static', image_path))
        
        # 创建讨论数据
        discussion_data = {
            'title': title,
            'content': content,
            'image_path': image_path,
            'created_by': user_id,
            'created_time': datetime.now(),
            'update_by': user_id,
            'update_time': datetime.now(),
            'is_deleted': 0
        }
        
        # 插入数据库
        result = user_discussion.add_discussion(discussion_data)
        
        if result.success:
            flash('讨论创建成功', 'success')
            
            # 创建用户-讨论映射关系
            mapping_data = {
                'user_id': user_id,
                'discuss_id': result.data['id'],
                'created_by': user_id,
                'update_by': user_id
            }
            user_mapping.add_mapping(mapping_data)
            
            return redirect(url_for('community.community'))
        else:
            flash(f'创建失败: {result.msg}', 'error')
    
    return render_template('community/create_discussion.html', id=user_id, active_page='community')

# 回复讨论
@community_bp.route('/discussion/<int:discussion_id>/reply', methods=['POST'])
def reply_discussion(discussion_id):
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'status': 'error', 'message': '请先登录'})
    
    content = request.form.get('content')
    parent_id = request.form.get('parent_id', 0)
    
    # 检查讨论是否存在
    discussion_response = user_discussion.get_discussion_by_id(discussion_id)
    
    if not discussion_response.success:
        return jsonify({'status': 'error', 'message': '讨论不存在或已被删除'})
    
    # 创建回复数据
    topic_data = {
        'parent_id': parent_id if int(parent_id) > 0 else None,
        'discussion_id': discussion_id,
        'content': content,
        'created_by': user_id,
        'created_time': datetime.now()
    }
    
    # 插入回复
    result = user_topic.add_topic(topic_data)
    
    if result.success:
        return jsonify({'status': 'success', 'message': '回复成功'})
    else:
        return jsonify({'status': 'error', 'message': f'回复失败: {result.msg}'})

# 删除讨论（软删除）
@community_bp.route('/discussion/<int:discussion_id>/delete', methods=['POST'])
def delete_discussion(discussion_id):
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'status': 'error', 'message': '请先登录'})
    
    # 检查是否是讨论的创建者
    discussion_response = user_discussion.get_discussion({
        'id': discussion_id,
        'created_by': user_id
    })
    
    if not discussion_response.success:
        return jsonify({'status': 'error', 'message': '无权删除此讨论'})
    
    # 软删除讨论
    update_data = {
        'is_deleted': 1,
        'update_by': user_id,
        'update_time': datetime.now()
    }
    
    result = user_discussion.update_discussion(discussion_id, update_data)
    
    if result.success:
        return jsonify({'status': 'success', 'message': '讨论已删除'})
    else:
        return jsonify({'status': 'error', 'message': f'删除失败: {result.msg}'})

# 搜索讨论
@community_bp.route('/search', methods=['GET'])
def search_discussions():
    user_id = session.get('user_id', '0')
    keyword = request.args.get('keyword', '')
    
    if not keyword:
        return redirect(url_for('community.community'))
    
    # 由于我们的模块不支持LIKE查询，这里需要获取所有未删除的讨论，然后在Python中过滤
    discussions_response = user_discussion.get_discussion({'is_deleted': 0})
    
    if discussions_response.success:
        all_discussions = discussions_response.data
        # 在Python中过滤包含关键词的讨论
        discussions = []
        for discussion in all_discussions:
            if (keyword.lower() in discussion['title'].lower() or 
                keyword.lower() in discussion['content'].lower()):
                # 获取回复数量
                replies_response = user_topic.get_topics_for_discussion(discussion['id'])
                discussion['reply_count'] = len(replies_response.data) if replies_response.success else 0
                # 获取作者名称
                discussion['author_name'] = discussion['created_by']
                discussions.append(discussion)
    else:
        discussions = []
    
    return render_template('community/search_results.html', discussions=discussions, keyword=keyword, id=user_id, active_page='community')