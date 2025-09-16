// navbar.js - 导航栏相关的JavaScript功能

// 使用立即执行函数避免变量污染全局作用域
(function() {
    // 立即初始化用户下拉菜单，不等待DOMContentLoaded
    initUserDropdown();
    
    // 等待DOM完全加载后初始化其他功能
    document.addEventListener('DOMContentLoaded', function() {
        console.log('navbar.js 加载完成');
        
        // 再次初始化用户下拉菜单（双重保险）
        initUserDropdown();
        
        // 处理移动端菜单
        initMobileMenu();
        
        // 处理平滑滚动
        initSmoothScroll();
    });
    
    // 用户下拉菜单初始化
    function initUserDropdown() {
        console.log('尝试初始化用户下拉菜单');
        
        // 使用setTimeout确保在Vue渲染后执行
        setTimeout(function() {
            const userAvatarToggle = document.getElementById('userAvatarToggle');
            const userDropdown = document.getElementById('userDropdown');
            
            if (userAvatarToggle && userDropdown) {
                console.log('找到用户下拉菜单元素');
                
                // 移除可能已存在的点击事件（通过克隆节点）
                const newUserAvatarToggle = userAvatarToggle.cloneNode(true);
                userAvatarToggle.parentNode.replaceChild(newUserAvatarToggle, userAvatarToggle);
                
                // 添加新的点击事件
                newUserAvatarToggle.addEventListener('click', function(e) {
                    console.log('点击了用户头像');
                    e.stopPropagation();
                    newUserAvatarToggle.classList.toggle('active');
                    userDropdown.classList.toggle('show');
                });
                
                // 点击页面其他地方关闭下拉菜单
                document.addEventListener('click', function() {
                    if (userDropdown.classList.contains('show')) {
                        newUserAvatarToggle.classList.remove('active');
                        userDropdown.classList.remove('show');
                    }
                });
                
                // 防止点击下拉菜单内部时关闭菜单
                userDropdown.addEventListener('click', function(e) {
                    e.stopPropagation();
                });
            } else {
                console.log('未找到用户下拉菜单元素');
            }
        }, 500); // 延迟500毫秒，确保DOM已完全渲染
    }
    
    // 移动端菜单初始化
    function initMobileMenu() {
        // 定义全局函数，用于HTML onclick属性
        window.toggleMobileMenu = function() {
            const mobileMenu = document.getElementById('mobileMenu');
            if (mobileMenu) {
                mobileMenu.classList.toggle('active');
            }
        };
        
        window.closeMobileMenu = function() {
            const mobileMenu = document.getElementById('mobileMenu');
            if (mobileMenu) {
                mobileMenu.classList.remove('active');
            }
        };
        
        // 添加移动菜单切换按钮的点击事件
        const menuToggle = document.querySelector('.menu-toggle');
        if (menuToggle) {
            menuToggle.addEventListener('click', window.toggleMobileMenu);
        }
    }
    
    // 平滑滚动初始化
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
})();