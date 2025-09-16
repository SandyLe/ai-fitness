// 判断当前模式
darkModeHandler()
NProgress.start();
$(window).load(function () {
  // 图片懒加载
  $("img").lazyload();
  $.scrollUp({
    scrollName: "scrollUp",
    topDistance: "300",
    topSpeed: 300,
    animation: "fade",
    animationInSpeed: 200,
    animationOutSpeed: 200,
    scrollText: '<i class="fa fa-angle-up"></i>',
    activeOverlay: !1
  });
  NProgress.done();
});
// 点击邮件中的链接跳转至相应评论
if(window.location.hash){
  var checkExist = setInterval(function() {
    if ($(window.location.hash).length) {
      $('html, body').animate({scrollTop: $(window.location.hash).offset().top-180}, 1000);
      clearInterval(checkExist);
    }
  }, 100);
}
$(".base_msg").css({
  display: 'flex'
});
let close_base_msg = sessionStorage.getItem('close_base_msg');
if (close_base_msg) {
  $(".base_msg").hide();
}
$(".close_base_msg").click(function () {
  $(".base_msg").hide();
  sessionStorage.setItem('close_base_msg', true);
})
function darkModeHandler() {
  DarkReader.setFetchMethod(window.fetch)
  DarkReader.auto({
    brightness: 100,
    contrast: 90,
    sepia: 0
  });
}
function closeKeyup() {
  document.onkeydown = function () {
    var e = window.event || arguments[0];
    if (e.keyCode == 123 || e.keyCode == 80) {
      return false;
    } else if ((e.ctrlKey) && (e.shiftKey) && (e.keyCode == 73)) {
      return false;
    } else if ((e.shiftKey) && (e.keyCode == 121)) {
      return false;
    } else if ((e.ctrlKey) && (e.keyCode == 85)) {
      return false;
    }
  };
  //取消鼠标右键
  document.oncontextmenu = function () {
    return true;
  }
}
function getQueryString(name) {
  let reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
  let r = window.location.search.substr(1).match(reg);
  if (r != null) return decodeURIComponent(r[2]);
  return null;
}
const hideBili = getQueryString('h')
const blibili = 'b'
if(hideBili === blibili) localStorage.setItem('hideBili', 1)
const div = document.createElement('div')
div.innerHTML = `<style type="text/css">
body {
font-size: 16px;
line-height: 16px;
letter-spacing: -4px;
}
pre {
display: block;
margin: 100px auto;
width: 250px;
overflow: hidden;
background-color: transparent;
border-color: transparent;
}

</style>
<pre>....................../´¯/)
....................,/¯../
.................../..../
............./´¯/'...'/´¯¯\`·¸
........../'/.../..../......./¨¯\\
........('(...´...´.... ¯~/'...')
.........\\.................'...../
..........''...\\.......... _.·´
............\\..............(
..............\\.............\\...</pre>`
const closeConsoleBan = localStorage.getItem('closeConsoleBan');
if (closeConsoleBan) {
  if ($('#article-content')) {
    $('#article-content').append('<a class="aHaAHa">编辑</a>')
  }
  $('.right-tool').hide();
  ConsoleBan.init({clear: false, debug: false})
} else {
  ConsoleBan.init({write: div})
  closeKeyup();
}
var n = 0;
$(".footer-section-desc").click(function () {n++;if (n === 6) {localStorage.setItem('closeConsoleBan', true);location.reload()}})
const closeRightTool = sessionStorage.getItem('closeRightTool');
if (closeRightTool) {
  $(".right-tool").hide()
}
$(".close").click(function () {
  $(".right-tool").hide()
  sessionStorage.setItem('closeRightTool', true)
})
$(".model-close-btn").click(function() {
  $('#myModal').modal('hide')
})
