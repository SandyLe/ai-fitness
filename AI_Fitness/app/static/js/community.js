// 社区模块通用 JavaScript 功能

document.addEventListener('DOMContentLoaded', function() {
    // 讨论过滤器功能
    const filterButtons = document.querySelectorAll('.filter-btn');
    if (filterButtons.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                // 移除所有按钮的 active 类
                filterButtons.forEach(btn => btn.classList.remove('active'));
                // 为当前按钮添加 active 类
                this.classList.add('active');
                
                const filter = this.getAttribute('data-filter');
                filterDiscussions(filter);
            });
        });
    }
    
    // 点赞功能
    const likeButtons = document.querySelectorAll('.like-btn');
    if (likeButtons.length > 0) {
        likeButtons.forEach(button => {
            button.addEventListener('click', function() {
                this.classList.toggle('active');
                const countElement = this.querySelector('.count');
                if (countElement) {
                    let count = parseInt(countElement.textContent);
                    if (this.classList.contains('active')) {
                        countElement.textContent = count + 1;
                    } else {
                        countElement.textContent = Math.max(0, count - 1);
                    }
                }
            });
        });
    }
    
    // 分享功能
    const shareBtn = document.getElementById('shareBtn');
    const shareModal = document.getElementById('shareModal');
    if (shareBtn && shareModal) {
        shareBtn.addEventListener('click', function() {
            shareModal.style.display = 'flex';
        });
    }
    
    // 举报功能
    const reportBtn = document.getElementById('reportBtn');
    const reportModal = document.getElementById('reportModal');
    if (reportBtn && reportModal) {
        reportBtn.addEventListener('click', function() {
            reportModal.style.display = 'flex';
        });
    }
    
    // 删除功能
    const deleteBtn = document.getElementById('deleteBtn');
    const deleteModal = document.getElementById('deleteModal');
    if (deleteBtn && deleteModal) {
        deleteBtn.addEventListener('click', function() {
            deleteModal.style.display = 'flex';
        });
    }
    
    // 确认删除
    const confirmDelete = document.getElementById('confirmDelete');
    if (confirmDelete) {
        confirmDelete.addEventListener('click', function() {
            const discussionId = deleteBtn.getAttribute('data-id');
            
            fetch(`/community/discussion/${discussionId}/delete`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    window.location.href = '/community/';
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('删除失败，请稍后再试');
            });
        });
    }
    
    // 回复功能
    const replyForm = document.getElementById('replyForm');
    if (replyForm) {
        replyForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const discussionId = this.getAttribute('data-discussion-id');
            const content = document.getElementById('replyContent').value;
            const parentId = document.getElementById('parentId').value;
            
            if (!content.trim()) {
                alert('回复内容不能为空');
                return;
            }
            
            fetch(`/community/discussion/${discussionId}/reply`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    'content': content,
                    'parent_id': parentId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // 刷新页面显示新回复
                    window.location.reload();
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('回复失败，请稍后再试');
            });
        });
    }
    
    // 回复某条评论
    const replyToButtons = document.querySelectorAll('.reply-to-btn');
    const cancelReply = document.getElementById('cancelReply');
    if (replyToButtons.length > 0 && cancelReply) {
        replyToButtons.forEach(button => {
            button.addEventListener('click', function() {
                const replyId = this.getAttribute('data-id');
                document.getElementById('parentId').value = replyId;
                document.getElementById('replyContent').focus();
                document.getElementById('replyContent').placeholder = `回复 #${replyId}`;
                cancelReply.style.display = 'block';
                
                // 滚动到回复表单
                document.querySelector('.reply-form').scrollIntoView({ behavior: 'smooth' });
            });
        });
        
        cancelReply.addEventListener('click', function() {
            document.getElementById('parentId').value = 0;
            document.getElementById('replyContent').placeholder = '写下你的回复...';
            this.style.display = 'none';
        });
    }
    
    // 关闭所有模态框
    const closeModalButtons = document.querySelectorAll('.close-modal, .btn-cancel');
    if (closeModalButtons.length > 0) {
        closeModalButtons.forEach(button => {
            button.addEventListener('click', function() {
                const modals = document.querySelectorAll('.modal');
                modals.forEach(modal => {
                    modal.style.display = 'none';
                });
            });
        });
    }
    
    // 点击模态框外部关闭
    const modals = document.querySelectorAll('.modal');
    if (modals.length > 0) {
        modals.forEach(modal => {
            modal.addEventListener('click', function(e) {
                if (e.target === this) {
                    this.style.display = 'none';
                }
            });
        });
    }
    
    // 举报表单提交
    const reportForm = document.getElementById('reportForm');
    if (reportForm) {
        reportForm.addEventListener('submit', function(e) {
            e.preventDefault();
            alert('举报已提交，我们会尽快处理');
            document.getElementById('reportModal').style.display = 'none';
        });
    }
});

// 过滤讨论列表
function filterDiscussions(filter) {
    const discussionCards = document.querySelectorAll('.discussion-card');
    
    if (filter === 'all') {
        discussionCards.forEach(card => {
            card.style.display = 'flex';
        });
        return;
    }
    
    discussionCards.forEach(card => {
        // 这里根据实际数据结构进行过滤
        // 示例实现，实际应用中需要根据后端数据调整
        if (filter === 'popular') {
            // 假设回复数大于5的为热门
            const replyCount = parseInt(card.querySelector('.replies .count')?.textContent || '0');
            card.style.display = replyCount > 5 ? 'flex' : 'none';
        } else if (filter === 'recent') {
            // 假设最近一周的为最新
            // 实际应用中需要比较日期
            card.style.display = 'flex';
        } else if (filter === 'unanswered') {
            // 假设回复数为0的为未回复
            const replyCount = parseInt(card.querySelector('.replies .count')?.textContent || '0');
            card.style.display = replyCount === 0 ? 'flex' : 'none';
        }
    });
}