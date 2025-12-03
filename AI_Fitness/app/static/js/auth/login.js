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

        width: 420,
        height: 220,
        pieceSize: 56,
        tolerance: 16,
        pieceY: 40,
        pieceX: 12,
        handleX: 0,
        dragging: false,
        startClientX: 0,
        startHandleX: 0,
        status: '请将滑块拖动到图中正确位置',
        showTarget: false,
        images: [
            'https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1200&q=80',
            'https://ix-marketing.imgix.net/global.jpg?auto=format,compress&w=1200&q=80',
            'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1200&q=80',
            'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200&q=80'
        ],
        currentIndex: Math.floor(Math.random()*4),
        targetX: 0,


        verificationSuccess: false,
        formSubmitted: false, // 标记表单是否已提交
        captchaLoaded: false  // 新增：标记验证码资源是否已加载
    },
    computed: {
        currentImage() {
            return this.images[this.currentIndex]
        },
        imageWrapStyle() {
            return {
                position: 'relative', width: this.width+'px', height: this.height+'px',
                borderRadius: '6px', overflow: 'hidden', boxShadow: '0 6px 20px rgba(0,0,0,0.12)'
            }
        },
        imgStyle() {
            return { width:'100%', height:'100%', objectFit:'cover' }
        },
        targetStyle() {
            return {
                position:'absolute', left:this.targetX+'px', top:this.pieceY+'px',
                width:this.pieceSize+'px', height:this.pieceSize+'px',
                border:'2px dashed rgba(255,255,255,0.9)', transform:'translateY(-50%)'
            }
        },
        pieceStyle() {
            return {
                position:'absolute', left:this.pieceX+'px', top:'10px',
                width:this.pieceSize+'px', height:this.pieceSize+'px',
                background:'rgba(255,255,255,0.9)', boxShadow:'0 6px 22px rgba(0,0,0,0.25)',
                borderRadius:'4px', display:'flex', alignItems:'center', justifyContent:'center'
                }
        },
        trackStyle() {
            return { position:'relative', height:'44px', background:'#f1f1f1', borderRadius:'6px', overflow:'hidden' }
        },
        progressStyle() {
            return {
                position:'absolute', left:0, top:0, bottom:0,
                width: Math.min(this.handleX + 22, this.width)+'px'
            }
        },
        handleStyle() {
            return {
                position:'absolute', left:this.handleX+'px', top:'6px', width:'44px', height:'32px',
                borderRadius:'6px', background:'#a69f9e', boxShadow:'0 4px 12px rgba(0,0,0,0.15)', cursor:'grab'
            }
        }
    },
    mounted() {
        this.randomizeTarget()
        window.addEventListener('mousemove', this.onMove)
        window.addEventListener('mouseup', this.onEnd)
        window.addEventListener('touchmove', this.onMove, {passive:false})
        window.addEventListener('touchend', this.onEnd)
    },
    beforeDestroy() {
        // 移除全局事件监听
        window.removeEventListener('mousemove', this.onMove)
        window.removeEventListener('mouseup', this.onEnd)
        window.removeEventListener('touchmove', this.onMove)
        window.removeEventListener('touchend', this.onEnd)
    },
    methods: {// 新增：预加载验证码资源
        preloadCaptchaResources() {
            // 随机生成验证码图片和位置，但不显示弹窗
            this.captchaLoaded = true;
            this.showTarget = true;
        },
        closeCaptcha() {
            this.showCaptcha = false;
        },
        showSliderCaptcha() {
            // 验证表单
            if (!this.loginForm.username || !this.loginForm.password) {
                alert('请填写用户名和密码');
                return;
            }
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
        randomizeTarget() {
            const min = Math.round(this.width * 0.12)
            const max = Math.round(this.width * 0.78)
            this.targetX = Math.floor(Math.random()*(max-min+1))+min
        },
        reset() {
            this.randomizeTarget()
            this.handleX = 0
            this.pieceX = 12
            this.status = '请将滑块拖动到图中正确位置'
        },
        nextImage() {
            this.currentIndex = (this.currentIndex + 1) % this.images.length
            this.reset()
        },
        onStart(e) {
            if (this.status.includes('成功')) return
            this.dragging = true
            this.startClientX = e.touches ? e.touches[0].clientX : e.clientX
            this.startHandleX = this.handleX
        },
        onMove(e) {
            if (!this.dragging) return
            e.preventDefault()
            const clientX = e.touches ? e.touches[0].clientX : e.clientX
            const dx = clientX - this.startClientX
            const maxX = this.width - 44
            let nx = this.startHandleX + dx
            nx = Math.max(0, Math.min(maxX, nx))
            this.handleX = nx
            const mapped = Math.round((nx / maxX) * (this.width - this.pieceSize - 8)) + 8
            this.pieceX = mapped
        },
        onEnd() {
            if (!this.dragging) return
            this.dragging = false
            const delta = Math.abs(this.pieceX - this.targetX)
            if (delta <= this.tolerance) {
                this.status = '验证成功 ✅'
                this.pieceX = this.targetX
                this.handleX = Math.round((this.targetX - 8)/(this.width - this.pieceSize - 8)*(this.width - 44))

                // 1.5秒后自动关闭验证码并提交表单
                setTimeout(() => {
                    this.closeCaptcha();
                    this.submitLogin();
                }, 1500);
            } else {
                this.status = '验证失败，请重试'
                this.handleX = 0
                this.pieceX = 12
            }
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