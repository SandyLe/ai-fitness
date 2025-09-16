// 创建讨论页面专用 JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // 图片预览功能
    const imageInput = document.getElementById('image');
    const imagePreview = document.getElementById('imagePreview');
    const previewImage = imagePreview.querySelector('img');
    const imagePlaceholder = imagePreview.querySelector('.image-placeholder');
    
    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    previewImage.src = e.target.result;
                    previewImage.style.display = 'block';
                    imagePlaceholder.style.display = 'none';
                }
                
                reader.readAsDataURL(this.files[0]);
            } else {
                previewImage.style.display = 'none';
                imagePlaceholder.style.display = 'flex';
            }
        });
    }
    
    // 标签功能
    const tagInput = document.getElementById('tagInput');
    const tagsContainer = document.getElementById('tagsContainer');
    const tagsHiddenInput = document.getElementById('tags');
    const tagSuggestions = document.querySelectorAll('.tag-suggestion');
    
    if (tagInput && tagsContainer && tagsHiddenInput) {
        // 存储已添加的标签
        const tags = [];
        
        // 更新隐藏输入框的值
        function updateTagsInput() {
            tagsHiddenInput.value = JSON.stringify(tags);
        }
        
        // 添加标签
        function addTag(tagText) {
            tagText = tagText.trim();
            
            // 检查是否为空或已存在
            if (tagText === '' || tags.includes(tagText)) {
                return;
            }
            
            // 限制标签数量
            if (tags.length >= 5) {
                alert('最多添加5个标签');
                return;
            }
            
            // 添加到数组
            tags.push(tagText);
            
            // 创建标签元素
            const tagElement = document.createElement('div');
            tagElement.className = 'tag-item';
            tagElement.innerHTML = `
                ${tagText}
                <span class="tag-remove" data-tag="${tagText}">&times;</span>
            `;
            
            // 添加到容器
            tagsContainer.appendChild(tagElement);
            
            // 清空输入框
            tagInput.value = '';
            
            // 更新隐藏输入
            updateTagsInput();
            
            // 添加删除事件
            const removeBtn = tagElement.querySelector('.tag-remove');
            removeBtn.addEventListener('click', function() {
                const tagToRemove = this.getAttribute('data-tag');
                removeTag(tagToRemove, tagElement);
            });
        }
        
        // 删除标签
        function removeTag(tagText, element) {
            // 从数组中移除
            const index = tags.indexOf(tagText);
            if (index !== -1) {
                tags.splice(index, 1);
            }
            
            // 从DOM中移除
            element.remove();
            
            // 更新隐藏输入
            updateTagsInput();
        }
        
        // 输入框回车事件
        tagInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                addTag(this.value);
            }
        });
        
        // 标签建议点击事件
        tagSuggestions.forEach(suggestion => {
            suggestion.addEventListener('click', function() {
                const tagText = this.getAttribute('data-tag');
                addTag(tagText);
            });
        });
    }
    
    // 预览功能
    const previewBtn = document.querySelector('.btn-preview');
    const previewModal = document.getElementById('previewModal');
    const previewTitle = document.getElementById('previewTitle');
    const previewContent = document.getElementById('previewContent');
    const previewImageContainer = document.getElementById('previewImage');
    const previewTags = document.getElementById('previewTags');
    
    if (previewBtn && previewModal) {
        previewBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const title = document.getElementById('title').value;
            const content = document.getElementById('content').value;
            const imageFile = document.getElementById('image').files[0];
            
            if (!title || !content) {
                alert('请填写标题和内容');
                return;
            }
            
            // 设置预览内容
            previewTitle.textContent = title;
            previewContent.textContent = content;
            
            // 设置预览图片
            if (imageFile) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewImageContainer.querySelector('img').src = e.target.result;
                    previewImageContainer.style.display = 'block';
                }
                reader.readAsDataURL(imageFile);
            } else {
                previewImageContainer.style.display = 'none';
            }
            
            // 设置预览标签
            previewTags.innerHTML = '';
            if (tagsHiddenInput && tagsHiddenInput.value) {
                try {
                    const tagsList = JSON.parse(tagsHiddenInput.value);
                    tagsList.forEach(tag => {
                        const tagSpan = document.createElement('span');
                        tagSpan.className = 'tag';
                        tagSpan.textContent = tag;
                        previewTags.appendChild(tagSpan);
                    });
                } catch (e) {
                    console.error('解析标签失败', e);
                }
            }
            
            // 显示预览模态框
            previewModal.style.display = 'flex';
        });
        
        // 确认发布按钮
        const publishBtn = document.querySelector('.btn-publish');
        if (publishBtn) {
            publishBtn.addEventListener('click', function() {
                document.querySelector('form').submit();
            });
        }
    }
});