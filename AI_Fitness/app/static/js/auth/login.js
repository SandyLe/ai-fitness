// 登录页面脚本
new Vue({
    el: '#login-page',
    data: {
        loginForm: {
            username: '',
            password: '',
            remember: false
        },
        showCaptcha: false,  // 确保初始值为false
        // 使用本地图片资源
        captchaConfig: {
            backgrounds: [
                // 使用本地背景图片
                '/static/img/captcha/bg1.jpg',
                '/static/img/captcha/bg2.jpg',
                // '/static/img/captcha/bg3.jpg',
                // '/static/img/captcha/bg4.jpg',
                // '/static/img/captcha/bg5.jpg'
            ],
            puzzles: [
                // 使用本地拼图形状
                '/static/img/captcha/puzzle_1.png',
                // '/static/img/captcha/puzzle_2.png',
                // '/static/img/captcha/puzzle_3.png'
            ]
        },
        captchaBackground: '',
        captchaPuzzle: '',
        puzzlePosition: { x: 0, y: 0 },
        targetPosition: { x: 180, y: 70 }, // 目标位置
        sliderValue: 0,
        isDragging: false,
        startX: 0,
        captchaResult: '',
        captchaResultClass: '',
        sliderTip: '向右滑动完成验证',
        verificationSuccess: false,
        formSubmitted: false, // 标记表单是否已提交
        captchaLoaded: false  // 新增：标记验证码资源是否已加载
    },
    computed: {
        puzzleStyle() {
            return {
                left: this.puzzlePosition.x + 'px',
                top: this.puzzlePosition.y + 'px'
            };
        }
    },
    mounted() {
        // 预加载验证码资源但不显示验证码弹窗
        this.preloadCaptchaResources();
        
        // 添加全局事件监听
        document.addEventListener('mousemove', this.onMouseMove);
        document.addEventListener('mouseup', this.onMouseUp);
        document.addEventListener('touchmove', this.onTouchMove);
        document.addEventListener('touchend', this.onTouchEnd);
    },
    beforeDestroy() {
        // 移除全局事件监听
        document.removeEventListener('mousemove', this.onMouseMove);
        document.removeEventListener('mouseup', this.onMouseUp);
        document.removeEventListener('touchmove', this.onTouchMove);
        document.removeEventListener('touchend', this.onTouchEnd);
    },
    methods: {
        // 新增：预加载验证码资源
        preloadCaptchaResources() {
            // 随机生成验证码图片和位置，但不显示弹窗
            this.generateRandomCaptcha();
            this.captchaLoaded = true;
        },
        
        showSliderCaptcha() {
            // 验证表单
            if (!this.loginForm.username || !this.loginForm.password) {
                alert('请填写用户名和密码');
                return;
            }
            
            // 重置验证码状态
            this.sliderValue = 0;
            this.puzzlePosition.x = 0;
            this.captchaResult = '';
            this.captchaResultClass = '';
            this.verificationSuccess = false;
            this.sliderTip = '向右滑动完成验证';
            
            // 随机生成新的验证码
            this.generateRandomCaptcha();
            
            // 确保资源加载完成后再显示验证码弹窗
            if (this.captchaLoaded) {
                this.showCaptcha = true;
            } else {
                // 如果资源未加载完成，先加载资源再显示弹窗
                this.preloadCaptchaResources();
                setTimeout(() => {
                    this.showCaptcha = true;
                }, 100);
            }
        },
        
        closeCaptcha() {
            this.showCaptcha = false;
        },
        
        generateRandomCaptcha() {
            // 随机选择背景图片
            const bgIndex = Math.floor(Math.random() * this.captchaConfig.backgrounds.length);
            this.captchaBackground = this.captchaConfig.backgrounds[bgIndex];
            
            // 随机选择拼图
            const puzzleIndex = Math.floor(Math.random() * this.captchaConfig.puzzles.length);
            this.captchaPuzzle = this.captchaConfig.puzzles[puzzleIndex];
            
            // 随机生成目标位置 (确保在合理范围内)
            this.targetPosition = {
                x: Math.floor(Math.random() * 150) + 100,
                y: Math.floor(Math.random() * 100) + 50
            };
            
            // 重置拼图初始位置
            this.puzzlePosition = { x: 0, y: this.targetPosition.y };
        },
        
        startSlide(event) {
            this.isDragging = true;
            
            // 记录起始位置
            if (event.type === 'mousedown') {
                this.startX = event.clientX;
            } else if (event.type === 'touchstart') {
                this.startX = event.touches[0].clientX;
            }
            
            // 阻止默认行为和事件冒泡
            event.preventDefault();
            event.stopPropagation();
        },
        
        onMouseMove(event) {
            if (!this.isDragging) return;
            
            this.moveSlider(event.clientX);
        },
        
        onTouchMove(event) {
            if (!this.isDragging) return;
            
            this.moveSlider(event.touches[0].clientX);
            event.preventDefault(); // 防止页面滚动
        },
        
        moveSlider(clientX) {
            // 计算移动距离
            const deltaX = clientX - this.startX;
            
            // 计算新的滑块位置 (限制在0-100%范围内)
            const containerWidth = document.querySelector('.slider-track').offsetWidth - 40; // 减去滑块宽度
            let newValue = (this.sliderValue * containerWidth / 100 + deltaX) / containerWidth * 100;
            newValue = Math.max(0, Math.min(100, newValue));
            
            // 更新滑块位置
            this.sliderValue = newValue;
            
            // 更新拼图位置 (等比例映射到目标x坐标)
            this.puzzlePosition.x = (newValue / 100) * this.targetPosition.x;
            
            // 更新起始位置
            this.startX = clientX;
        },
        
        onMouseUp() {
            if (!this.isDragging) return;
            
            this.finishSlide();
        },
        
        onTouchEnd() {
            if (!this.isDragging) return;
            
            this.finishSlide();
        },
        
        finishSlide() {
            this.isDragging = false;
            
            // 检查是否验证成功 (允许10px的误差)
            const isSuccess = Math.abs(this.puzzlePosition.x - this.targetPosition.x) < 10;
            
            if (isSuccess) {
                this.captchaResult = '验证成功！';
                this.captchaResultClass = 'success';
                this.sliderTip = '验证通过';
                this.verificationSuccess = true;
                
                // 1.5秒后自动关闭验证码并提交表单
                setTimeout(() => {
                    this.closeCaptcha();
                    this.submitLogin();
                }, 1500);
            } else {
                this.captchaResult = '验证失败，请重试';
                this.captchaResultClass = 'error';
                
                // 重置滑块位置
                setTimeout(() => {
                    this.sliderValue = 0;
                    this.puzzlePosition.x = 0;
                    this.captchaResult = '';
                }, 1000);
            }
        },
        
        submitLogin() {
            // 防止重复提交
            if (this.formSubmitted) return;
            this.formSubmitted = true;
            
            // 创建一个隐藏的表单并提交
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '/login';
            form.style.display = 'none';
            
            // 添加用户名字段
            const usernameInput = document.createElement('input');
            usernameInput.type = 'hidden';
            usernameInput.name = 'username';
            usernameInput.value = this.loginForm.username;
            form.appendChild(usernameInput);
            
            // 添加密码字段
            const passwordInput = document.createElement('input');
            passwordInput.type = 'hidden';
            passwordInput.name = 'password';
            passwordInput.value = this.loginForm.password;
            form.appendChild(passwordInput);
            
            // 添加记住我字段
            const rememberInput = document.createElement('input');
            rememberInput.type = 'hidden';
            rememberInput.name = 'remember';
            rememberInput.value = this.loginForm.remember ? '1' : '0';
            form.appendChild(rememberInput);
            
            // 添加验证成功标志
            const verificationInput = document.createElement('input');
            verificationInput.type = 'hidden';
            verificationInput.name = 'verification_success';
            verificationInput.value = this.verificationSuccess ? '1' : '0';
            form.appendChild(verificationInput);
            
            // 添加到页面并提交
            document.body.appendChild(form);
            form.submit();
        }
        
        // showMessage 方法保持不变
    }
});