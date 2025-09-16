// footer.js - 页脚相关的JavaScript功能

document.addEventListener('DOMContentLoaded', function() {
    // 社交媒体图标交互效果
    const socialIcons = document.querySelectorAll('.social-icon');
    if (socialIcons) {
        socialIcons.forEach(icon => {
            icon.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-3px)';
            });
            
            icon.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });
    }
    
    // APP下载按钮交互效果
    const appButtons = document.querySelectorAll('.app-button');
    if (appButtons) {
        appButtons.forEach(button => {
            button.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.05)';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
            });
        });
    }
    
    // 页脚链接平滑滚动效果
    document.querySelectorAll('.footer-links a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});