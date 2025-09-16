function updateTime() {
    var now = new Date();

    var year = now.getFullYear();
    var month = now.getMonth() + 1;
    var day = now.getDate();
    var week = now.getDay();
    var weekArray = ["日", "一", "二", "三", "四", "五", "六"];
    var hours = now.getHours();
    var minutes = now.getMinutes();
    var seconds = now.getSeconds();

    // 格式化时间
    hours = hours < 10 ? '0' + hours : hours;
    minutes = minutes < 10 ? '0' + minutes : minutes;
    seconds = seconds < 10 ? '0' + seconds : seconds;

    var timeString = hours + ':' + minutes + ':' + seconds;
    var dateString = year + '年' + month + '月' + day + '日';
    var weekString = '星期' + weekArray[week];

    document.getElementById("clock").innerText = timeString;
    document.getElementById("date").innerText = dateString + ' ' + weekString;
}

// 每秒更新一次时间
setInterval(updateTime, 1000);

// 页面加载时立即更新时间
updateTime();