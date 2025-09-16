// 全局变量
let webcamElement;
let canvasElement;
let canvasCtx;
let pose;
let camera;
let exerciseType = '';
let counter = 0;
let flag = 0;
let isRunning = false;

// DOM元素
let exerciseNameElement;
let counterElement;
let guideTextElement;
let exerciseSelectElement;
let startButton;
let stopButton;
let resetButton;

// 初始化函数
function init() {
    // 获取DOM元素
    webcamElement = document.getElementById('webcam');
    canvasElement = document.getElementById('output-canvas');
    canvasCtx = canvasElement.getContext('2d');
    
    exerciseNameElement = document.getElementById('exercise-name');
    counterElement = document.getElementById('counter');
    guideTextElement = document.getElementById('guide-text');
    exerciseSelectElement = document.getElementById('exercise-select');
    startButton = document.getElementById('start-btn');
    stopButton = document.getElementById('stop-btn');
    resetButton = document.getElementById('reset-btn');
    
    // 设置事件监听器
    exerciseSelectElement.addEventListener('change', function() {
        exerciseType = this.value;
        exerciseNameElement.textContent = exerciseType || '未选择';
    });
    
    startButton.addEventListener('click', startDetection);
    stopButton.addEventListener('click', stopDetection);
    resetButton.addEventListener('click', resetCounter);
    
    // 初始化MediaPipe Pose
    initPose();
}

// 初始化MediaPipe Pose
function initPose() {
    pose = new Pose({
        locateFile: (file) => {
            return `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`;
        }
    });
    
    pose.setOptions({
        modelComplexity: 1,
        smoothLandmarks: true,
        enableSegmentation: false,
        smoothSegmentation: false,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5
    });
    
    pose.onResults(onResults);
    
    // 设置相机
    camera = new Camera(webcamElement, {
        onFrame: async () => {
            if (isRunning) {
                await pose.send({image: webcamElement});
            }
        },
        width: 640,
        height: 480
    });
}

// 开始检测
function startDetection() {
    if (!exerciseType) {
        alert('请先选择一个训练动作');
        return;
    }
    
    if (!isRunning) {
        isRunning = true;
        camera.start();
        guideTextElement.textContent = '开始！';
    }
}

// 停止检测
function stopDetection() {
    if (isRunning) {
        isRunning = false;
        camera.stop();
    }
}

// 重置计数器
function resetCounter() {
    counter = 0;
    counterElement.textContent = counter;
}

// 处理姿态检测结果
function onResults(results) {
    // 调整画布大小
    canvasElement.width = webcamElement.videoWidth;
    canvasElement.height = webcamElement.videoHeight;
    
    // 清除画布
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
    
    // 绘制摄像头画面
    canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);
    
    // 如果检测到姿态，绘制骨架并分析动作
    if (results.poseLandmarks) {
        // 绘制骨架
        drawConnectors(canvasCtx, results.poseLandmarks, POSE_CONNECTIONS, {color: '#00FF00', lineWidth: 4});
        drawLandmarks(canvasCtx, results.poseLandmarks, {color: '#FF0000', lineWidth: 2, radius: 6});
        
        // 提取关键点
        const keypoints = extractKeypoints(results.poseLandmarks);
        
        // 分析动作
        const result = analyzeExercise(keypoints, exerciseType);
        const newCount = result.counter;
        const guideText = result.guideText;
        
        // 更新计数器
        if (newCount > 0) {
            counter += newCount;
            counterElement.textContent = counter;
        }
        
        // 更新指导文本
        if (guideText) {
            guideTextElement.textContent = guideText;
        }
    }
}

// 提取关键点
function extractKeypoints(landmarks) {
    const keypoints = [];
    const indices = [0, 1, 4, 7, 8, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28];
    
    for (let i = 0; i < indices.length; i++) {
        const idx = indices[i];
        const x = landmarks[idx].x * canvasElement.width;
        const y = landmarks[idx].y * canvasElement.height;
        keypoints.push([x, y]);
    }
    
    return keypoints;
}

// 计算两个向量之间的角度
function getAngle(v1, v2) {
    // 计算点积
    const dotProduct = v1[0] * v2[0] + v1[1] * v2[1];
    // 计算向量长度
    const v1Mag = Math.sqrt(v1[0] * v1[0] + v1[1] * v1[1]);
    const v2Mag = Math.sqrt(v2[0] * v2[0] + v2[1] * v2[1]);
    // 计算角度（弧度）
    const angle = Math.acos(dotProduct / (v1Mag * v2Mag));
    // 转换为角度
    let angleDeg = angle * 180 / Math.PI;
    
    // 确定角度方向
    const cross = v2[0] * v1[1] - v2[1] * v1[0];
    if (cross < 0) {
        angleDeg = -angleDeg;
    }
    
    return angleDeg;
}

// 分析运动
function analyzeExercise(keypoints, type) {
    let counter = 0;
    let guideText = "开始！";
    
    // 计算各种角度
    // 右臂与水平方向的夹角
    const v1_right_arm = [keypoints[5][0] - keypoints[6][0], keypoints[5][1] - keypoints[6][1]];
    const v2_right_arm = [keypoints[8][0] - keypoints[6][0], keypoints[8][1] - keypoints[6][1]];
    const angle_right_arm = getAngle(v1_right_arm, v2_right_arm);
    
    // 左臂与水平方向的夹角
    const v1_left_arm = [keypoints[7][0] - keypoints[5][0], keypoints[7][1] - keypoints[5][1]];
    const v2_left_arm = [keypoints[6][0] - keypoints[5][0], keypoints[6][1] - keypoints[5][1]];
    const angle_left_arm = getAngle(v1_left_arm, v2_left_arm);
    
    // 右肘的夹角
    const v1_right_elbow = [keypoints[6][0] - keypoints[8][0], keypoints[6][1] - keypoints[8][1]];
    const v2_right_elbow = [keypoints[10][0] - keypoints[8][0], keypoints[10][1] - keypoints[8][1]];
    const angle_right_elbow = Math.abs(getAngle(v1_right_elbow, v2_right_elbow));
    
    // 左肘的夹角
    const v1_left_elbow = [keypoints[5][0] - keypoints[7][0], keypoints[5][1] - keypoints[7][1]];
    const v2_left_elbow = [keypoints[9][0] - keypoints[7][0], keypoints[9][1] - keypoints[7][1]];
    const angle_left_elbow = Math.abs(getAngle(v1_left_elbow, v2_left_elbow));
    
    // 左大腿和左臂夹角
    const v1_left_leg = [keypoints[13][0] - keypoints[11][0], keypoints[13][1] - keypoints[11][1]];
    const v2_left_leg = [keypoints[7][0] - keypoints[5][0], keypoints[7][1] - keypoints[5][1]];
    const angle_left_leg = getAngle(v1_left_leg, v2_left_leg);
    
    // 右大腿和右臂夹角
    const v1_right_leg = [keypoints[14][0] - keypoints[12][0], keypoints[14][1] - keypoints[12][1]];
    const v2_right_leg = [keypoints[8][0] - keypoints[6][0], keypoints[8][1] - keypoints[6][1]];
    const angle_right_leg = getAngle(v1_right_leg, v2_right_leg);
    
    // 左大腿和左小腿夹角
    const v1_left_knee = [keypoints[11][0] - keypoints[13][0], keypoints[11][1] - keypoints[13][1]];
    const v2_left_knee = [keypoints[15][0] - keypoints[13][0], keypoints[15][1] - keypoints[13][1]];
    const angle_left_knee = getAngle(v1_left_knee, v2_left_knee);
    
    // 右大腿和右小腿夹角
    const v1_right_knee = [keypoints[12][0] - keypoints[14][0], keypoints[12][1] - keypoints[14][1]];
    const v2_right_knee = [keypoints[16][0] - keypoints[14][0], keypoints[16][1] - keypoints[14][1]];
    const angle_right_knee = getAngle(v1_right_knee, v2_right_knee);
    
    // v8-v6-v12
    const v1_v8_v6_v12 = [keypoints[8][0] - keypoints[6][0], keypoints[8][1] - keypoints[6][1]];
    const v2_v8_v6_v12 = [keypoints[12][0] - keypoints[6][0], keypoints[12][1] - keypoints[6][1]];
    const angle_v8_v6_v12 = Math.abs(getAngle(v1_v8_v6_v12, v2_v8_v6_v12));
    
    // v6_v12_v14
    const v1_v6_v12_v14 = [keypoints[6][0] - keypoints[12][0], keypoints[6][1] - keypoints[12][1]];
    const v2_v6_v12_v14 = [keypoints[14][0] - keypoints[12][0], keypoints[14][1] - keypoints[12][1]];
    const angle_v6_v12_v14 = Math.abs(getAngle(v1_v6_v12_v14, v2_v6_v12_v14));
    
    // v6_V8_v10
    const v1_v6_V8_v10 = [keypoints[6][0] - keypoints[8][0], keypoints[6][1] - keypoints[8][1]];
    const v2_v6_V8_v10 = [keypoints[10][0] - keypoints[8][0], keypoints[10][1] - keypoints[8][1]];
    const angle_v6_V8_v10 = Math.abs(getAngle(v1_v6_V8_v10, v2_v6_V8_v10));
    
    // v5_v7_v9
    const v1_v5_v7_v9 = [keypoints[5][0] - keypoints[7][0], keypoints[5][1] - keypoints[7][1]];
    const v2_v5_v7_v9 = [keypoints[9][0] - keypoints[7][0], keypoints[9][1] - keypoints[7][1]];
    const angle_v5_v7_v9 = Math.abs(getAngle(v1_v5_v7_v9, v2_v5_v7_v9));
    
    // v12_v14_v16
    const v1_v12_v14_v16 = [keypoints[12][0] - keypoints[14][0], keypoints[12][1] - keypoints[14][1]];
    const v2_v12_v14_v16 = [keypoints[16][0] - keypoints[14][0], keypoints[16][1] - keypoints[14][1]];
    const angle_v12_v14_v16 = Math.abs(getAngle(v1_v12_v14_v16, v2_v12_v14_v16));
    
    // v11_v13_v15
    const v1_v11_v13_v15 = [keypoints[11][0] - keypoints[13][0], keypoints[11][1] - keypoints[13][1]];
    const v2_v11_v13_v15 = [keypoints[15][0] - keypoints[13][0], keypoints[15][1] - keypoints[13][1]];
    const angle_v11_v13_v15 = Math.abs(getAngle(v1_v11_v13_v15, v2_v11_v13_v15));
    
    // 定义各种动作的条件
    // 哑铃推肩条件
    const shoulder_push_begin = (angle_right_leg > -90 && angle_left_leg < 90);
    const shoulder_push_finish = (angle_right_leg < -150 && angle_left_leg > 150);
    
    // 哑铃飞鸟条件
    const flying_bird_begin = (angle_right_leg > -30 && angle_left_leg < 30);
    const flying_bird_finish = (angle_right_leg < -60 && angle_left_leg > 60);
    
    // 哑铃深蹲条件
    const squat_begin = (angle_left_knee < -120 || angle_left_knee > 0);
    const squat_finish = (angle_left_knee > -70 && angle_left_knee < 0);
    
    // 哑铃二头弯举条件
    const bend_begin = (angle_left_elbow < 180 && angle_left_elbow > 150 && angle_right_elbow < 180 && angle_right_elbow > 150);
    const bend_finish = (angle_left_elbow < 20 && angle_left_elbow > 0 && angle_right_elbow < 20 && angle_right_elbow > 0);
    const bend_in = (angle_left_elbow > 20 && angle_left_elbow < 150 && angle_right_elbow > 20 && angle_right_elbow < 150);
    const bend_a = (angle_left_elbow > 150 && angle_left_elbow < 180 && angle_right_elbow > 150 && angle_right_elbow < 180);
    const bend_b = (angle_left_elbow > 0 && angle_left_elbow < 20 && angle_right_elbow > 0 && angle_right_elbow < 20);
    
    // 哑铃上斜卧推条件
    const Incline_bench_press_begin = (angle_v8_v6_v12 < 90 && angle_v8_v6_v12 > 50);
    const Incline_bench_press_finish = (angle_v8_v6_v12 > 165 && angle_v8_v6_v12 < 180);
    
    // 哑铃练侧腹
    const Fellers_begin = (angle_v8_v6_v12 > 0 && angle_v8_v6_v12 < 10);
    const Fellers_finish = (angle_v8_v6_v12 > 110 && angle_v8_v6_v12 < 150);
    
    // 哑铃仰卧起坐
    const yaling_yangwqz_begin = (angle_v6_v12_v14 > 170 && angle_v6_v12_v14 < 180);
    const yaling_yangwqz_finish = (angle_v6_v12_v14 > 90 && angle_v6_v12_v14 < 140);
    
    // 哑铃划船
    const yaling_rhuachuan_begin = (angle_v6_V8_v10 > 150 && angle_v6_V8_v10 < 180);
    const yaling_rhuachuan_finish = (angle_v6_V8_v10 < 95 && angle_v6_V8_v10 > 10);
    const yaling_lhuachuan_begin = (angle_v5_v7_v9 > 150 && angle_v5_v7_v9 < 180);
    const yaling_lhuachuan_finish = (angle_v5_v7_v9 < 95 && angle_v5_v7_v9 > 10);
    
    // 躺姿哑铃臂屈伸
    const yaling_qubishen_begin = (angle_left_elbow < 180 && angle_left_elbow > 150 && angle_right_elbow < 180 && angle_right_elbow > 150);
    const yaling_qubishen_finish = (angle_left_elbow < 60 && angle_left_elbow > 0 && angle_right_elbow < 60 && angle_right_elbow > 0);
    
    // 哑铃早安鞠躬挺
    const yaling_gongting_begin = (angle_v6_v12_v14 > 90 && angle_v6_v12_v14 < 140);
    const yaling_gongting_finish = (angle_v6_v12_v14 > 170 && angle_v6_v12_v14 < 180);
    
    // 哑铃保加利亚单腿深蹲左
    const squatl_begin = (angle_v12_v14_v16 > 160 && angle_v12_v14_v16 < 180);
    const squatl_finish = (angle_v12_v14_v16 > 0 && angle_v12_v14_v16 < 160);
    
    // 哑铃保加利亚单腿深蹲右
    const squatr_begin = (angle_v11_v13_v15 > 160 && angle_v11_v13_v15 < 180);
    const squatr_finish = (angle_v11_v13_v15 > 0 && angle_v11_v13_v15 < 160);
    
    // 根据不同动作类型判断
    switch (type) {
        case "哑铃推肩":
            if (shoulder_push_begin) {
                flag = 1;
            } else if (shoulder_push_finish && flag) {
                counter = 1;
                flag = 0;
            }
            break;
        case "哑铃飞鸟":
            if (flying_bird_begin) {
                flag = 1;
            } else if (flying_bird_finish && flag) {
                counter = 1;
                flag = 0;
            }
            break;
        case "高脚杯深蹲":
            if (squat_begin) {
                flag = 1;
            } else if (squat_finish && flag) {
                counter = 1;
                flag = 0;
            }
            break;
        case "哑铃二头弯举":
            if (bend_begin) {
                flag = 1;
            } else if (bend_finish && flag) {
                counter = 1;
                flag = 0;
            }
            if (bend_a) {
                guideText = "请缓慢抬起双手手臂！！";
            } else if (bend_b) {
                guideText = "完成了，非常棒！！";
            } else if (bend_in && flag) {
                guideText = "再抬高一点！！";
            }
            break;
        case "哑铃上斜卧推":
            if (Incline_bench_press_begin) {
                flag = 1;
            } else if (Incline_bench_press_finish && flag) {
                counter = 1;
                flag = 0;
            }
            break;
        case "哑铃砍伐者":
            if (Fellers_begin) {
                flag = 1;
            } else if (Fellers_finish && flag) {
                counter = 1;
                flag = 0;
            }
            break;
        case "哑铃仰卧起坐":
            if (yaling_yangwqz_begin) {
                flag = 1;
            } else if (yaling_yangwqz_finish && flag) {
                counter = 1;
                flag = 0;
            }
            break;
        case "右手哑铃划船":
            if (yaling_rhuachuan_begin) {
                flag = 1;
            } else if (yaling_rhuachuan_finish && flag) {
                counter = 1;
                flag = 0;
            }
            break;
        case "左手哑铃划船":
            if (yaling_lhuachuan_begin) {
                flag = 1;
            } else if (yaling_lhuachuan_finish && flag) {
                counter = 1;
                flag = 0;
            }
            break;
        case "躺姿哑铃臂屈伸":
            if (yaling_qubishen_begin) {
                flag = 1;
            } else if (yaling_qubishen_finish && flag) {
                counter = 1;
                flag = 0;
            }
            break;
        case "哑铃早安鞠躬挺":
            if (yaling_gongting_begin) {
                flag = 1;
            } else if (yaling_gongting_finish && flag) {
                counter = 1;
                flag = 0;
            }
            break;
        case "哑铃保加利亚单腿深蹲左":
            if (squatl_begin) {
                flag = 1;
            } else if (squatl_finish && flag) {
                counter = 1;
                flag = 0;
            }
            break;
        case "哑铃保加利亚单腿深蹲右":
            if (squatr_begin) {
                flag = 1;
            } else if (squatr_finish && flag) {
                counter = 1;
                flag = 0;
            }
            break;
    }
    
    return { counter, guideText };
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', init);