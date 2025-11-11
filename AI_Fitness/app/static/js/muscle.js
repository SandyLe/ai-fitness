window.onload = function() {
    // 初始化选中的器材类型
    var section_button_el = document.getElementsByClassName('section-button');
    let type_url = getQueryString("type_url");
    if(type_url) localStorage.setItem('type_url', type_url);
    
    var type_url_by_local = type_url || localStorage.getItem("type_url") || "dumbbell";
    
    // 设置默认选中的器材按钮
    for (let i=0; i<section_button_el.length; i++) {
        let cur_data = section_button_el[i].getAttribute("data-name");
        if(cur_data == type_url_by_local) {
            section_button_el[i].classList.add("section-selected");
            section_button_el[i].classList.add("active"); // 添加active类
        } else {
            section_button_el[i].classList.remove("section-selected");
            section_button_el[i].classList.remove("active"); // 移除active类
        }
    }
    
    // 如果没有选中的按钮，默认选中第一个
    if (!document.querySelector('.section-selected') && section_button_el.length > 0) {
        section_button_el[0].classList.add("section-selected");
        section_button_el[0].classList.add("active"); // 添加active类
        localStorage.setItem('type_url', section_button_el[0].getAttribute("data-name"));
    }
    
    // 初始化性别选择
    var _sex = localStorage.getItem("sex") || "m";
    if (_sex === "m") {
        document.getElementById("femalefigures").style.display = "none";
        document.getElementById("malefigures").style.display = "block";
        // 添加男性按钮选中状态
        document.getElementById("sexchoosermalelabel").classList.add("active");
        document.getElementById("sexchooserfemalelabel").classList.remove("active");
    } else {
        document.getElementById("malefigures").style.display = "none";
        document.getElementById("femalefigures").style.display = "block";
        // 添加女性按钮选中状态
        document.getElementById("sexchooserfemalelabel").classList.add("active");
        document.getElementById("sexchoosermalelabel").classList.remove("active");
    }
//    alert(document.getElementById("streak-days").innerHTML)
}

document.onclick = function(event) {
    var el = event.target;
    
    // 处理器材选择按钮点击
    if (el.classList.contains("section-button")) {
        if(document.getElementsByClassName('section-selected')[0]) {
            document.getElementsByClassName('section-selected')[0].classList.remove("section-selected");
            document.getElementsByClassName('section-selected')[0]?.classList.remove("active");
        }
        
        // 移除所有按钮的active类
        var allButtons = document.querySelectorAll('.section-button');
        allButtons.forEach(function(btn) {
            btn.classList.remove("active");
        });
        
        el.classList.add("section-selected");
        el.classList.add("active"); // 添加active类
        localStorage.setItem('type_url', el.getAttribute("data-name"));
        event.stopPropagation();
        return;
    }
    
    // 处理性别选择按钮点击
    if (hasInParentsUntil(event.target, 'sexchoosermalelabel', document)) {
        document.getElementById("femalefigures").style.display = "none";
        document.getElementById("malefigures").style.display = "block";
        localStorage.setItem("sex", "m");
        
        // 更新性别按钮选中状态
        document.getElementById("sexchoosermalelabel").classList.add("active");
        document.getElementById("sexchooserfemalelabel").classList.remove("active");
        
        $("#mobilebg").attr('src', $(this).data('src'));
        event.stopPropagation();
        return;
    }
    
    if (hasInParentsUntil(event.target, 'sexchooserfemalelabel', document)) {
        document.getElementById("malefigures").style.display = "none";
        document.getElementById("femalefigures").style.display = "block";
        localStorage.setItem("sex", "f");
        
        // 更新性别按钮选中状态
        document.getElementById("sexchooserfemalelabel").classList.add("active");
        document.getElementById("sexchoosermalelabel").classList.remove("active");
        
        $("#mobilebg-female").attr('src', $(this).data('src'));
        $("#background-female").attr('src', $(this).data('src'));
        event.stopPropagation();
        return;
    }
    
    // 处理肌肉图像点击
    if (el.nodeName == "IMG" && el.id && el.id !== "background" && el.id !== "background-female" && 
        el.id !== "mobilebg" && el.id !== "mobilebg-female") {
        
        // 获取性别参数
        var gender = localStorage.getItem("sex") || "m";
        var genderParam = gender === "m" ? "man" : "woman";
        
        // 获取器材参数
        var selectedButton = document.querySelector('.section-selected');
        var equipmentParam = selectedButton ? selectedButton.getAttribute('data-name') : "dumbbell";
        
        // 根据肌肉ID确定肌肉参数
        var muscleParam = getMuscleParam(el.id);
        
        // 如果成功识别肌肉，跳转到对应页面
        if (muscleParam) {
            console.log(`跳转到: /fitness/${muscleParam}/${genderParam}/${equipmentParam}`);
            window.location.href = `/fitness/${muscleParam}/${genderParam}/${equipmentParam}`;
        } else {
            console.error("未能识别肌肉ID: " + el.id);
        }
    }
};

// 根据肌肉ID获取对应的肌肉参数
function getMuscleParam(muscleId) {
    // 胸部肌肉
    if (muscleId === "pecs" || muscleId === "female-pecs") {
        return "Chest";
    }
    
    // 肩部肌肉
    if (muscleId.includes("shoulders") || muscleId.includes("back-shoulders")) {
        return "Shoulders";
    }
    
    // 斜方肌
    if (muscleId === "back-traps-b" || muscleId === "female-back-traps-b") {
        return "Traps_middle";
    }
    if (muscleId.includes("traps") || muscleId.includes("back-traps")) {
        return "Traps";
    }
    
    // 二头肌
    if (muscleId.includes("biceps")) {
        return "Biceps";
    }
    
    // 三头肌
    if (muscleId.includes("triceps")) {
        return "Triceps";
    }
    
    // 前臂
    if (muscleId.includes("forearm") || muscleId.includes("back-forearms")) {
        return "Forearms";
    }
    
    // 腹肌
    if (muscleId === "obliques" || muscleId === "female-abdominals") {
        return "Abdominals";
    }
    
    // 侧腹
    if (muscleId.includes("obliques-") || muscleId.includes("female-obliques-")) {
        return "Flanks";
    }
    
    // 背阔肌
    if (muscleId.includes("back-lats") || muscleId.includes("back-upper")) {
        return "Lats";
    }
    
    // 下背部
    if (muscleId === "back-lower" || muscleId === "female-back-lower") {
        return "Lowerback";
    }
    
    // 臀部
    if (muscleId === "back-glutes" || muscleId === "female-back-glutes") {
        return "Glutes";
    }
    
    // 大腿前侧
    if (muscleId.includes("quads")) {
        return "Quads";
    }
    
    // 大腿后侧
    if (muscleId.includes("hamstrings")) {
        return "Hamstrings";
    }
    
    // 小腿
    if (muscleId.includes("calves")) {
        return "Calves";
    }
    
    return null;
}

function resizeIframe(obj) {
    obj.style.height = obj.contentWindow.document.body.scrollHeight + 'px';
}

function getQueryString(name) {
    let reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    let r = window.location.search.substr(1).match(reg);
    if (r != null) return decodeURIComponent(r[2]);
    return null;
}

function hasInParentsUntil(el, id, limit) {
    while (el && el !== limit) {
        if (el.id === id) return true;
        el = el.parentNode;
    }
    return false;
}

// 在文件末尾添加以下代码

// 排行榜和打卡功能
document.addEventListener('DOMContentLoaded', function() {
    // 获取排行榜切换按钮
    const tabButtons = document.querySelectorAll('.tab-btn');
    
    // 为每个按钮添加点击事件
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // 移除所有按钮的active类
            tabButtons.forEach(btn => btn.classList.remove('active'));
            
            // 为当前点击的按钮添加active类
            this.classList.add('active');
            
            // 获取当前点击按钮的类型
            const type = this.getAttribute('data-type');
            
            // 隐藏所有排行榜
            document.querySelectorAll('.leaderboard-list').forEach(list => {
                list.classList.remove('active');
            });
            
            // 显示对应类型的排行榜
            document.querySelector(`.${type}-leaderboard`).classList.add('active');
        });
    });
    
    // 打卡按钮功能
    const clockBtn = document.querySelector('.clock-btn');
    if (clockBtn) {
        clockBtn.addEventListener('click', function() {
            // 更新打卡状态
            const statusValue = document.querySelector('.status-value');
            if (statusValue.textContent === '未打卡') {
                statusValue.textContent = '已打卡';
                statusValue.style.color = '#4caf50';
                statusValue.style.backgroundColor = '#e8f5e9';
                this.textContent = '今日已打卡';
                this.disabled = true;
                this.style.background = 'linear-gradient(to right, #9e9e9e, #bdbdbd)';
                this.style.cursor = 'default';
                
                // 更新连续打卡天数
                const streakDays = document.querySelector('.streak-days');
                const newStreakDays = parseInt(streakDays.textContent) + 1;
                streakDays.textContent = newStreakDays;
                
                // 更新进度条
                const progressFill = document.querySelector('.progress-fill');
                const progressText = document.querySelector('.progress-text');
                const currentProgress = progressText.textContent.match(/(\d+)\/(\d+)/);
                if (currentProgress) {
                    const current = parseInt(currentProgress[1]) + 1;
                    const total = parseInt(currentProgress[2]);
                    const percentage = (current / total) * 100;
                    progressFill.style.width = `${percentage}%`;
                    progressText.textContent = `本月打卡：${current}/${total}天`;
                }
                
                // 添加打卡动画效果
                const clockSection = document.querySelector('.clock-section');
                clockSection.classList.add('pulse-animation');
                setTimeout(() => {
                    clockSection.classList.remove('pulse-animation');
                }, 1000);
                
                // 显示打卡成功提示
                showToast('打卡成功！继续保持！');
            }
        });
    }
    
    // 添加排行榜项目悬停效果
    const leaderboardItems = document.querySelectorAll('.leaderboard-item');
    leaderboardItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });
    
    // 显示提示消息的函数
    function showToast(message) {
        // 创建toast元素
        const toast = document.createElement('div');
        toast.className = 'toast-message';
        toast.textContent = message;
        
        // 添加到页面
        document.body.appendChild(toast);
        
        // 显示动画
        setTimeout(() => {
            toast.classList.add('show');
        }, 10);
        
        // 自动消失
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(toast);
            }, 300);
        }, 3000);
    }
    
    // 添加Toast样式
    const style = document.createElement('style');
    style.textContent = `
        .toast-message {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background-color: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 16px;
            z-index: 9999;
            opacity: 0;
            transition: all 0.3s ease;
        }
        
        .toast-message.show {
            transform: translateX(-50%) translateY(0);
            opacity: 1;
        }
        
        .pulse-animation {
            animation: pulse 1s;
        }
        
        @keyframes pulse {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.05);
            }
            100% {
                transform: scale(1);
            }
        }
    `;
    document.head.appendChild(style);
});
