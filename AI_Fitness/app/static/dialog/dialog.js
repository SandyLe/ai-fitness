/* ========================================================
   jQuery 插件：modalInput（增强版）
   支持：
   - 多字段（input / textarea / select / radio）
   - 多实例
   - 三种动画 fade / zoom / slide
   - 每字段校验
   - 全局回调
======================================================== */

;(function($){

  var pluginName = "modalInput";

  var defaults = {
    title: "请输入",
    fields: [],   // 字段数组
    animation: "zoom",   // fade | zoom | slide

    okText: "确定",
    cancelText: "取消",

    // 返回 { valid:bool, msg:"" }
    onConfirm: function(values){},
    onClose: function(){}
  };

  function ModalInput(element, options){
    this.$trigger = $(element);
    this.options = $.extend(true, {}, defaults, options);
    this._build();
    this._bindEvents();
  }

  ModalInput.prototype._build = function(){
    var id = "mi_" + Math.random().toString(36).substr(2,8);

    this.$mask = $(`
      <div class="mi-mask ${this.options.animation}" id="${id}">
        <div class="mi-box">
          <div class="mi-title"></div>
          <div class="mi-fields"></div>
          <div class="mi-footer">
            <button class="mi-btn mi-btn-cancel"></button>
            <button class="mi-btn mi-btn-ok"></button>
          </div>
        </div>
      </div>
    `);

    $("body").append(this.$mask);

    this.$title = this.$mask.find(".mi-title");
    this.$fields = this.$mask.find(".mi-fields");
    this.$btnCancel = this.$mask.find(".mi-btn-cancel");
    this.$btnOk = this.$mask.find(".mi-btn-ok");
  };

  /** 构建字段 DOM */
  ModalInput.prototype._renderFields = function(){
    var fieldsHTML = "";
    var fields = this.options.fields;

    fields.forEach((f,i)=>{
      fieldsHTML += `<div class="mi-field" data-index="${i}">
        <label class="mi-label">${f.label || ""}</label>`;

      if (f.type === "text"){
        fieldsHTML += `<input class="mi-input" type="text" value="${f.default || ""}" placeholder="${f.placeholder||""}">`;
      }

      if (f.type === "textarea"){
        fieldsHTML += `<textarea class="mi-textarea" placeholder="${f.placeholder||""}">${f.default||""}</textarea>`;
      }

      if (f.type === "select"){
        fieldsHTML += `<select class="mi-select">`;
        f.options.forEach(o=>{
          fieldsHTML += `<option value="${o.value}" ${o.value===f.default?"selected":""}>${o.label}</option>`;
        });
        fieldsHTML += `</select>`;
      }

      if (f.type === "radio"){
        fieldsHTML += `<div class="mi-radio-group">`;
        f.options.forEach(o=>{
          var checked = (o.value===f.default) ? "checked" : "";
          fieldsHTML += `
            <label>
              <input type="radio" name="mi_radio_${i}" value="${o.value}" ${checked}> ${o.label}
            </label>`;
        });
        fieldsHTML += `</div>`;
      }

      fieldsHTML += `<div class="mi-error"></div></div>`;
    });

    this.$fields.html(fieldsHTML);
  };

  ModalInput.prototype._bindEvents = function(){
    var self = this;

    this.$trigger.on("click", function(){
      self.open();
    });

    this.$mask.on("click", function(e){
      if (e.target === self.$mask[0]) self.close();
    });

    this.$btnCancel.on("click", ()=>self.close());

    this.$btnOk.on("click", function(){
      var values = {};
      var valid = true;

      self.$fields.find(".mi-field").each(function(){
        var index = $(this).data("index");
        var f = self.options.fields[index];
        var $error = $(this).find(".mi-error");
        $error.hide();

        var value;

        if (f.type === "text")      value = $(this).find("input").val().trim();
        if (f.type === "textarea") value = $(this).find("textarea").val().trim();
        if (f.type === "select")   value = $(this).find("select").val();
        if (f.type === "radio")    value = $(this).find('input[type="radio"]:checked').val();

        if (f.validate){
          var r = f.validate(value);
          if (!r.valid){
            $error.text(r.msg||"输入有误").show();
            valid = false;
            return;
          }
        }

        values[f.name] = value;
      });

      if (!valid) return;

      self.options.onConfirm(values);
      self.close();
    });

    $(document).on("keydown", function(e){
      if (!self.$mask.hasClass("show")) return;
      if (e.key === "Escape") self.close();
    });
  };

  ModalInput.prototype.open = function(){
    this.$title.text(this.options.title);
    this.$btnCancel.text(this.options.cancelText);
    this.$btnOk.text(this.options.okText);

    this._renderFields();

    this.$mask.addClass("show");
  };

  ModalInput.prototype.close = function(){
    this.$mask.removeClass("show");
    this.options.onClose();
  };

  ModalInput.prototype.destroy = function(){
    this.$mask.remove();
    this.$trigger.off("click");
    this.$trigger.removeData(pluginName);
  };

  $.fn[pluginName] = function(options){
    return this.each(function(){
      if (!$.data(this, pluginName)) {
        $.data(this, pluginName, new ModalInput(this, options));
      }
    });
  };

})(jQuery);
