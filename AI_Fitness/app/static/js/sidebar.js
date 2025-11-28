// 等待文档完全加载
document.addEventListener('DOMContentLoaded', function() {
    var sidebar = document.getElementById('sidebar');
    var toggleBtn = document.getElementById('toggleBtn');
    var sidebarContent = document.getElementById('sidebarContent');
    
    // 点击页面任何地方的事件处理
    document.addEventListener('click', function(event) {
      // 检查点击事件发生的位置是否在侧拉框以外，并且侧拉框是打开状态
      if (!sidebar.contains(event.target) && event.target !== toggleBtn && sidebar.style.left === '40px') {
        sidebar.style.left = '-100%'; // 关闭侧拉框
      }
    });
    
    // 切换按钮点击事件
    toggleBtn.addEventListener('click', function(event) {
      // 阻止事件冒泡，防止立即触发document的click事件
      event.stopPropagation();
      
      // 使用静态路径替代模板语法
      var staticbasepath = '../../../static/';
      
      // 添加动态生成的 HTML 内容
      sidebarContent.innerHTML = `
        <link rel="stylesheet" href="${staticbasepath}css/baseBig.min_for_sidebar.css">
        <link rel="stylesheet" href="${staticbasepath}css/base.musclewiki.min_for_sidebar.css">
        <div class="mw-content-text">
        <div class="row content-menu">
            <div id="sex-choice-wrapper" class="col-xs-12 col-sm-12 col-md-3 col-lg-3">
                <h4 class="choice-title">选择性别</h4>
                <div class="btn-group fitness-choice" data-toggle="buttons">
                        <label class="btn fitness-btn gender-btn" id="sexchoosermalelabel">
                            <input type="radio" name="sexchooser" id="sexchoosermale" value="male" checked="">
                            <img src="${staticbasepath}images/gender/male.png" class="gender-icon">
                            <span>男士</span>
                        </label>
                        <label class="btn fitness-btn gender-btn" id="sexchooserfemalelabel">
                            <input type="radio" name="sexchooser" id="sexchooserfemale" value="female">
                            <img src="${staticbasepath}images/gender/female.png" class="gender-icon">
                            <span>女士</span>
                        </label>
                </div>
            </div>
            <div id="section_options" class="col-xs-12 col-sm-12 col-md-9 col-lg-9">
                <h4 class="choice-title">选择科室</h4>
                <div class="equipment-container">
                    <button data-name="Exercises" class="section-button equipment-btn">
                        <img src="${staticbasepath}images/equipment/dumbbell.png" class="equipment-icon">外科
                    </button>
                    <button data-name="Stretches" class="section-button equipment-btn">
                        <img src="${staticbasepath}images/equipment/stretch.png" class="equipment-icon">拉伸
                    </button>
                    <button data-name="Bodyweight" class="section-button equipment-btn">
                        <img src="${staticbasepath}images/equipment/bodyweight.png" class="equipment-icon">徒手
                    </button>
                    <button data-name="Kettlebells" class="section-button equipment-btn">
                        <img src="${staticbasepath}images/equipment/kettlebell.png" class="equipment-icon">壶铃
                    </button>
                    <button data-name="Barbell" class="section-button equipment-btn">
                        <img src="${staticbasepath}images/equipment/barbell.png" class="equipment-icon">杠铃
                    </button>
                    <button data-name="Gantry" class="section-button equipment-btn">
                        <img src="${staticbasepath}images/equipment/gantry.png" class="equipment-icon">龙门架
                    </button>
                    <button data-name="Band" class="section-button equipment-btn">
                        <img src="${staticbasepath}images/equipment/band.png" class="equipment-icon">弹力带
                    </button>
                </div>
            </div>
        </div>
        <div id="malefigures">
                <div id="mobile-muscle-map">
                    <img id="mobilebg" src="${staticbasepath}Crops1/mobilebg.png ">
                    <img id="traps-a" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" 
                        data-src="${staticbasepath}Crops1/08.-TrapsLeft.png ">
                    <img id="traps-b" src="${staticbasepath}Crops1/08.-TrapsRight.png ">
                    <img id="shoulders-a" src="${staticbasepath}Crops1/07.A-Deltoids.png ">
                    <img id="shoulders-b" src="${staticbasepath}Crops1/07.B-Deltoids.png ">
                    <img id="pecs" src="${staticbasepath}Crops1/06.-Pecs.png ">
                    <img id="biceps-a" src="${staticbasepath}Crops1/05.A-Biceps.png ">
                    <img id="biceps-b" src="${staticbasepath}Crops1/05.B-Biceps.png ">
                    <img id="forearm-a" src="${staticbasepath}Crops1/14.A-Forearms.png ">
                    <img id="forearm-b" src="${staticbasepath}Crops1/14.B-Forearms.png ">
                    <img id="obliques" src="${staticbasepath}Crops1/04.-Obliques.png ">
                    <img id="quads-a" src="${staticbasepath}Crops1/01.A-Quads.png ">
                    <img id="quads-b" src="${staticbasepath}Crops1/01.B-Quads.png ">
                    <img id="calves-a" src="${staticbasepath}Crops1/13.A-Calves.png ">
                    <img id="calves-b" src="${staticbasepath}Crops1/13.B-Calves.png ">
                    <img id="back-traps-a" src="${staticbasepath}Crops1/08.B-Traps.png ">
                    <img id="back-traps-b" src="${staticbasepath}Crops1/08.C-Traps.png ">
                    <img id="back-shoulders-a" src="${staticbasepath}Crops1/07.C-Deltoids.png ">
                    <img id="back-shoulders-b" src="${staticbasepath}Crops1/07.D-Deltoids.png ">
                    <img id="triceps-a" src="${staticbasepath}Crops1/09.A-Triceps.png ">
                    <img id="triceps-b" src="${staticbasepath}Crops1/09.B-Triceps.png ">
                    <img id="back-lats-a" src="${staticbasepath}Crops1/10.A-Lats.png ">
                    <img id="back-lats-b" src="${staticbasepath}Crops1/10.B-Lats.png ">
                    <img id="back-lower" src="${staticbasepath}Crops1/15.-Lower-Back.png ">
                    <img id="back-forearms-a" src="${staticbasepath}Crops1/14.C-Forearms.png ">
                    <img id="back-forearms-b" src="${staticbasepath}Crops1/14.D-Forearms.png ">
                    <img id="back-glutes" src="${staticbasepath}Crops1/11.-Glutes.png ">
                    <img id="back-hamstrings-a" src="${staticbasepath}Crops1/12.A-Hamstrings.png ">
                    <img id="back-hamstrings-b" src="${staticbasepath}Crops1/12.B-Hamstrings.png ">
                    <img id="back-calves-a" src="${staticbasepath}Crops1/13.C-Calves.png ">
                    <img id="back-calves-b" src="${staticbasepath}Crops1/13.D-Calves.png ">
                    <img id="obliques-a" src="${staticbasepath}Crops1/16.A-Obliques.png ">
                    <img id="obliques-b" src="${staticbasepath}Crops1/16.B-Obliques.png ">
                </div>
                <div id="muscle-map">
                    <img id="background" alt="Logo" src="${staticbasepath}Crops1/00.-Blank-Figures.png ">
                    <img id="traps-a" src="${staticbasepath}Crops1/08.-TrapsLeft.png ">
                    <img id="traps-b" src="${staticbasepath}Crops1/08.-TrapsRight.png ">
                    <img id="shoulders-a" src="${staticbasepath}Crops1/07.A-Deltoids.png ">
                    <img id="shoulders-b" src="${staticbasepath}Crops1/07.B-Deltoids.png ">
                    <img id="pecs" src="${staticbasepath}Crops1/06.-Pecs.png ">
                    <img id="biceps-a" src="${staticbasepath}Crops1/05.A-Biceps.png ">
                    <img id="biceps-b" src="${staticbasepath}Crops1/05.B-Biceps.png ">
                    <img id="forearm-a" src="${staticbasepath}Crops1/14.A-Forearms.png ">
                    <img id="forearm-b" src="${staticbasepath}Crops1/14.B-Forearms.png ">
                    <img id="obliques" src="${staticbasepath}Crops1/04.-Obliques.png ">
                    <img id="quads-a" src="${staticbasepath}Crops1/01.A-Quads.png ">
                    <img id="quads-b" src="${staticbasepath}Crops1/01.B-Quads.png ">
                    <img id="calves-a" src="${staticbasepath}Crops1/13.A-Calves.png ">
                    <img id="calves-b" src="${staticbasepath}Crops1/13.B-Calves.png ">
                    <img id="back-traps-a" src="${staticbasepath}Crops1/08.B-Traps.png ">
                    <img id="back-traps-b" src="${staticbasepath}Crops1/08.C-Traps.png ">
                    <img id="back-shoulders-a" src="${staticbasepath}Crops1/07.C-Deltoids.png ">
                    <img id="back-shoulders-b" src="${staticbasepath}Crops1/07.D-Deltoids.png ">
                    <img id="triceps-a" src="${staticbasepath}Crops1/09.A-Triceps.png ">
                    <img id="triceps-b" src="${staticbasepath}Crops1/09.B-Triceps.png ">
                    <img id="back-lats-a" src="${staticbasepath}Crops1/10.A-Lats.png ">
                    <img id="back-lats-b" src="${staticbasepath}Crops1/10.B-Lats.png ">
                    <img id="back-lower" src="${staticbasepath}Crops1/15.-Lower-Back.png ">
                    <img id="back-forearms-a" src="${staticbasepath}Crops1/14.C-Forearms.png ">
                    <img id="back-forearms-b" src="${staticbasepath}Crops1/14.D-Forearms.png ">
                    <img id="back-glutes" src="${staticbasepath}Crops1/11.-Glutes.png ">
                    <img id="back-hamstrings-a" src="${staticbasepath}Crops1/12.A-Hamstrings.png ">
                    <img id="back-hamstrings-b" src="${staticbasepath}Crops1/12.B-Hamstrings.png ">
                    <img id="back-calves-a" src="${staticbasepath}Crops1/13.C-Calves.png ">
                    <img id="back-calves-b" src="${staticbasepath}Crops1/13.D-Calves.png ">
                    <img id="obliques-a" src="${staticbasepath}Crops1/16.A-Obliques.png ">
                    <img id="obliques-b" src="${staticbasepath}Crops1/16.B-Obliques.png ">
                </div>
        </div>
        <div id="femalefigures">
                <div id="mobile-muscle-map-female">
                    <img id="mobilebg-female" src="${staticbasepath}Crops1/female/female-mobilebg.png ">
                    <img id="female-traps-a" src="${staticbasepath}Crops1/female/female-traps-A.png ">
                    <img id="female-traps-b" src="${staticbasepath}Crops1/female/female-traps-B.png ">
                    <img id="female-shoulders-a" src="${staticbasepath}Crops1/female/female-deltoids-A.png ">
                    <img id="female-shoulders-b" src="${staticbasepath}Crops1/female/female-deltoids-B.png ">
                    <img id="female-pecs" src="${staticbasepath}Crops1/female/female-pecs.png ">
                    <img id="female-biceps-a" src="${staticbasepath}Crops1/female/female-biceps-A.png ">
                    <img id="female-biceps-b" src="${staticbasepath}Crops1/female/female-biceps-B.png ">
                    <img id="female-forearm-a" src="${staticbasepath}Crops1/female/female-forearms-A.png ">
                    <img id="female-forearm-b" src="${staticbasepath}Crops1/female/female-forearms-B.png ">
                    <img id="female-abdominals" src="${staticbasepath}Crops1/female/female-abdominals.png ">
                    <img id="female-quads-a" src="${staticbasepath}Crops1/female/female-quads-A.png ">
                    <img id="female-quads-b" src="${staticbasepath}Crops1/female/female-quads-B.png ">
                    <img id="female-calves-a" src="${staticbasepath}Crops1/female/female-calves-A.png ">
                    <img id="female-calves-b" src="${staticbasepath}Crops1/female/female-calves-B.png ">
                    <img id="female-back-traps-a" src="${staticbasepath}Crops1/female/female-traps-C.png ">
                    <img id="female-back-traps-b" src="${staticbasepath}Crops1/female/female-traps-D.png ">
                    <img id="female-back-shoulders-a" src="${staticbasepath}Crops1/female/female-deltoids-C.png ">
                    <img id="female-back-shoulders-b" src="${staticbasepath}Crops1/female/female-deltoids-D.png ">
                    <img id="female-triceps-a" src="${staticbasepath}Crops1/female/female-triceps-A.png ">
                    <img id="female-triceps-b" src="${staticbasepath}Crops1/female/female-triceps-B.png ">
                    <img id="female-back-lats-a" src="${staticbasepath}Crops1/female/female-lats-A.png ">
                    <img id="female-back-lats-b" src="${staticbasepath}Crops1/female/female-lats-B.png ">
                    <img id="female-back-lower" src="${staticbasepath}Crops1/female/female-lowerback.png ">
                    <img id="female-back-forearms-a" src="${staticbasepath}Crops1/female/female-forearms-C.png ">
                    <img id="female-back-forearms-b" src="${staticbasepath}Crops1/female/female-forearms-D.png ">
                    <img id="female-back-glutes" src="${staticbasepath}Crops1/female/female-glutes.png ">
                    <img id="female-back-hamstrings-a" src="${staticbasepath}Crops1/female/female-hamstrings-A.png ">
                    <img id="female-back-hamstrings-b" src="${staticbasepath}Crops1/female/female-hamstrings-B.png ">
                    <img id="female-back-calves-a" src="${staticbasepath}Crops1/female/female-calves-C.png ">
                    <img id="female-back-calves-b" src="${staticbasepath}Crops1/female/female-calves-D.png ">
                    <img id="female-obliques-a" src="${staticbasepath}Crops1/female/female-obliques-A.png ">
                    <img id="female-obliques-b" src="${staticbasepath}Crops1/female/female-obliques-B.png ">
                </div>
                <div id="muscle-map-female">
                    <img id="background-female" src="${staticbasepath}Crops1/female/Female-Figures.png ">
                    <img id="female-traps-a" src="${staticbasepath}Crops1/female/female-traps-A.png ">
                    <img id="female-traps-b" src="${staticbasepath}Crops1/female/female-traps-B.png ">
                    <img id="female-shoulders-a" src="${staticbasepath}Crops1/female/female-deltoids-A.png ">
                    <img id="female-shoulders-b" src="${staticbasepath}Crops1/female/female-deltoids-B.png ">
                    <img id="female-pecs" src="${staticbasepath}Crops1/female/female-pecs.png ">
                    <img id="female-biceps-a" src="${staticbasepath}Crops1/female/female-biceps-A.png ">
                    <img id="female-biceps-b" src="${staticbasepath}Crops1/female/female-biceps-B.png ">
                    <img id="female-forearm-a" src="${staticbasepath}Crops1/female/female-forearms-A.png ">
                    <img id="female-forearm-b" src="${staticbasepath}Crops1/female/female-forearms-B.png ">
                    <img id="female-abdominals" src="${staticbasepath}Crops1/female/female-abdominals.png ">
                    <img id="female-quads-a" src="${staticbasepath}Crops1/female/female-quads-A.png ">
                    <img id="female-quads-b" src="${staticbasepath}Crops1/female/female-quads-B.png ">
                    <img id="female-calves-a" src="${staticbasepath}Crops1/female/female-calves-A.png ">
                    <img id="female-calves-b" src="${staticbasepath}Crops1/female/female-calves-B.png ">
                    <img id="female-back-traps-a" src="${staticbasepath}Crops1/female/female-traps-C.png ">
                    <img id="female-back-traps-b" src="${staticbasepath}Crops1/female/female-traps-D.png ">
                    <img id="female-back-shoulders-a" src="${staticbasepath}Crops1/female/female-deltoids-C.png ">
                    <img id="female-back-shoulders-b" src="${staticbasepath}Crops1/female/female-deltoids-D.png ">
                    <img id="female-triceps-a" src="${staticbasepath}Crops1/female/female-triceps-A.png ">
                    <img id="female-triceps-b" src="${staticbasepath}Crops1/female/female-triceps-B.png ">
                    <img id="female-back-lats-a" src="${staticbasepath}Crops1/female/female-lats-A.png ">
                    <img id="female-back-lats-b" src="${staticbasepath}Crops1/female/female-lats-B.png ">
                    <img id="female-back-lower" src="${staticbasepath}Crops1/female/female-lowerback.png ">
                    <img id="female-back-forearms-a" src="${staticbasepath}Crops1/female/female-forearms-C.png ">
                    <img id="female-back-forearms-b" src="${staticbasepath}Crops1/female/female-forearms-D.png ">
                    <img id="female-back-glutes" src="${staticbasepath}Crops1/female/female-glutes.png ">
                    <img id="female-back-hamstrings-a" src="${staticbasepath}Crops1/female/female-hamstrings-A.png ">
                    <img id="female-back-hamstrings-b" src="${staticbasepath}Crops1/female/female-hamstrings-B.png ">
                    <img id="female-back-calves-a" src="${staticbasepath}Crops1/female/female-calves-C.png ">
                    <img id="female-back-calves-b" src="${staticbasepath}Crops1/female/female-calves-D.png ">
                    <img id="female-obliques-a" src="${staticbasepath}Crops1/female/female-obliques-A.png ">
                    <img id="female-obliques-b" src="${staticbasepath}Crops1/female/female-obliques-B.png ">
                </div>
        </div>
    </div>
        `
    // 切换侧拉框的显示状态
    if (sidebar.style.left === '-100%' || sidebar.style.left === '') {
        sidebar.style.left = '40px';
        sidebar.style.borderRadius = '5%';
      } else {
        sidebar.style.left = '-100%';
      }
    });
    
    // 移除以下代码，不再自动触发按钮点击
    // window.onload = function() {
    //   toggleBtn.click();
    // };
  });