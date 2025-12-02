// 注册页面脚本
new Vue({
    el: '#forget-pwd-page',
    data: {
        registerForm: {
            username: '',
            email: '',
            password: '',
            confirmPassword: '',
            questionId: '',
            answer: '',
            gender: '',
            age: '',
            height: '',
            weight: '',
            agreeTerms: false
        },
        step: 0,
        usernameInputVisiable: true,
        emailInputVisiable: true,
        pwdInputVisiable: false,
        questionInputVisiable: false,
        passwordError: '',
        confirmPasswordError: '',
        termsError: '',
        confirmQuestionError: '',
        showCaptcha: false,  // 确保初始值为false
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
        nextStep() {
            if (this.step == 0) {
                this.questionInputVisiable = true;
                this.usernameInputVisiable = false;
                this.emailInputVisiable = false;
                this.step = 1;
            } else if (this.step == 1) {
                this.pwdInputVisiable = true;
                this.questionInputVisiable = false;
                this.step = 2;
                this.$refs.forgetBtn.textContent = '完成'
            } else if (this.step == 2) {
                this.pwdInputVisiable = true;
                this.questionInputVisiable = false;
                this.step = 2;
            }
        },
        validateAndRegister() {
            // 重置错误信息
            this.usernameError = '';
            this.emailError = '';
            this.passwordError = '';
            this.confirmPasswordError = '';
            this.termsError = '';
            this.confirmQuestionError = '';
            
            let isValid = true;
            let firstErrorField = null;
            
            // 验证用户名 (至少3个字符)
            if (!this.registerForm.username || this.registerForm.username.length < 3) {
                this.usernameError = '用户名至少需要3个字符';
                isValid = false;
                firstErrorField = 'usernameInput';
            }
            
            // 验证邮箱格式
            const emailRegex = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
            if (!this.registerForm.email || !emailRegex.test(this.registerForm.email)) {
                this.emailError = '请输入有效的电子邮箱地址';
                isValid = false;
                firstErrorField = firstErrorField || 'emailInput';
            }
            
            // 验证密码长度
            if (!this.registerForm.password || this.registerForm.password.length < 8) {
                this.passwordError = '密码至少需要8个字符';
                isValid = false;
                firstErrorField = firstErrorField || 'passwordInput';
            } else {
                // 验证密码是否包含字母和数字
                const hasLetter = /[a-zA-Z]/.test(this.registerForm.password);
                const hasNumber = /[0-9]/.test(this.registerForm.password);
                if (!hasLetter || !hasNumber) {
                    this.passwordError = '密码必须包含字母和数字';
                    isValid = false;
                    firstErrorField = firstErrorField || 'passwordInput';
                }
            }
            
            // 验证两次密码是否一致
            if (this.registerForm.password !== this.registerForm.confirmPassword) {
                this.confirmPasswordError = '两次输入的密码不一致';
                isValid = false;
                firstErrorField = firstErrorField || 'confirmPasswordInput';
            }
            //找回密码问题
            if (!this.registerForm.questionId) {
                this.confirmQuestionError = '请选择找回密码问题';
                isValid = false;
                firstErrorField = 'confirmQuestionInput';
            }
            // 验证是否同意条款
            if (!this.registerForm.agreeTerms) {
                this.termsError = '请同意服务条款和隐私政策';
                isValid = false;
                // 没有输入框可以聚焦，所以不设置firstErrorField
            }
            
            // 如果有错误，聚焦到第一个错误字段
            if (firstErrorField) {
                this.$nextTick(() => {
                    this.$refs[firstErrorField].focus();
                });
                return;
            }
            
            // 验证通过，显示验证码
            if (isValid) {
                this.showSliderCaptcha();
            }
        },
        
        // 提交注册请求
        submitRegister() {
            // 创建一个表单元素
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '/register';
            form.style.display = 'none';
            
            // 添加用户名字段
            const usernameInput = document.createElement('input');
            usernameInput.type = 'text';
            usernameInput.name = 'username';
            usernameInput.value = this.registerForm.username;
            form.appendChild(usernameInput);
            
            // 添加邮箱字段
            const emailInput = document.createElement('input');
            emailInput.type = 'email';
            emailInput.name = 'email';
            emailInput.value = this.registerForm.email;
            form.appendChild(emailInput);
            
            // 添加密码字段
            const passwordInput = document.createElement('input');
            passwordInput.type = 'password';
            passwordInput.name = 'password';
            passwordInput.value = this.registerForm.password;
            form.appendChild(passwordInput);
            
            // 添加确认密码字段
            const confirmPasswordInput = document.createElement('input');
            confirmPasswordInput.type = 'password';
            confirmPasswordInput.name = 'confirm_password';
            confirmPasswordInput.value = this.registerForm.confirmPassword;
            form.appendChild(confirmPasswordInput);

            // 添加提示问题字段
            const questionInput = document.createElement('input');
            questionInput.type = 'text';
            questionInput.name = 'questionId';
            questionInput.value = this.registerForm.questionId;
            form.appendChild(questionInput);

            // 添加答案字段
            const answerInput = document.createElement('input');
            answerInput.type = 'text';
            answerInput.name = 'answer';
            answerInput.value = this.registerForm.answer;
            form.appendChild(answerInput);

            // 添加性别字段
            const genderInput = document.createElement('input');
            genderInput.type = 'text';
            genderInput.name = 'gender';
            genderInput.value = this.registerForm.gender;
            form.appendChild(genderInput);

            // 添加年齡字段
            const ageInput = document.createElement('input');
            ageInput.type = 'text';
            ageInput.name = 'age';
            ageInput.value = this.registerForm.age;
            form.appendChild(ageInput);

            // 添加身高字段
            const heightInput = document.createElement('input');
            heightInput.type = 'text';
            heightInput.name = 'height';
            heightInput.value = this.registerForm.height;
            form.appendChild(heightInput);

            // 添加体重字段
            const weightInput = document.createElement('input');
            weightInput.type = 'text';
            weightInput.name = 'weight';
            weightInput.value = this.registerForm.weight;
            form.appendChild(weightInput);

            // 将表单添加到文档中并提交
            document.body.appendChild(form);
            form.submit();
        },
        
        // 新增：预加载验证码资源
        preloadCaptchaResources() {
            // 随机生成验证码图片和位置，但不显示弹窗
            this.generateRandomCaptcha();
            this.captchaLoaded = true;
        },
        
        showSliderCaptcha() {
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
            // 随机选择背景图片 (1-5)
            const bgIndex = Math.floor(Math.random() * 5) + 1;
            this.captchaBackground = `/static/img/captcha/bg${bgIndex}.jpg`;
            
            // 随机选择拼图 (1-3)
            const puzzleIndex = Math.floor(Math.random() * 3) + 1;
            this.captchaPuzzle = `/static/img/captcha/puzzle${puzzleIndex}.png`;
            
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
            
            this.isDragging = false;
            this.verifyCaptcha();
        },
        
        onTouchEnd() {
            if (!this.isDragging) return;
            
            this.isDragging = false;
            this.verifyCaptcha();
        },
        
        verifyCaptcha() {
            // 计算拼图与目标位置的误差
            const error = Math.abs(this.puzzlePosition.x - this.targetPosition.x);
            
            // 如果误差在可接受范围内，则验证成功
            if (error < 10) {
                this.captchaResult = '验证成功！';
                this.captchaResultClass = 'success';
                this.sliderTip = '验证通过';
                this.verificationSuccess = true;
                
                // 延迟关闭验证码弹窗并提交注册
                setTimeout(() => {
                    this.closeCaptcha();
                    this.submitRegister();
                }, 1000);
            } else {
                // 验证失败，重置验证码
                this.captchaResult = '验证失败，请重试';
                this.captchaResultClass = 'error';
                
                // 延迟重置
                setTimeout(() => {
                    this.sliderValue = 0;
                    this.puzzlePosition.x = 0;
                    this.captchaResult = '';
                }, 1000);
            }
        }
    }
});