/* ========================================================
   通用弹框组件：modalInput（无 trigger 版，供菜单/业务直接调用）
   特点：
   - 独立调用 openModalInput(options)
   - 支持多字段 / 校验 / 动画 / 回调
   - 不绑定点击源，不污染业务插件
======================================================== */
;(function($){

  var defaults = {
    title: "请输入",
    fields: [],
    animation: "zoom",   // fade | zoom | slide

    okText: "确定",
    cancelText: "取消",

    onConfirm: function(values){},
    onClose: function(){},
    onOpen: function(){}
  };

  function ModalInput(options){
    this.options = $.extend(true, {}, defaults, options);
    this._build();
    this._bindEvents();
  }

  ModalInput.prototype._build = function(){
    var id = "mi_" + Math.random().toString(36).substr(2,8);

    this.$mask = $(
      '<div class="mi-mask ' + this.options.animation + '" id="' + id + '">' +
        '<div class="mi-box">' +
          '<div class="mi-title"></div>' +
          '<div class="mi-fields"></div>' +
          '<div class="mi-footer">' +
            '<button class="mi-btn mi-btn-cancel"></button>' +
            '<button class="mi-btn mi-btn-ok"></button>' +
          '</div>' +
        '</div>' +
      '</div>'
    );

    $('body').append(this.$mask);

    this.$title = this.$mask.find('.mi-title');
    this.$fields = this.$mask.find('.mi-fields');
    this.$btnCancel = this.$mask.find('.mi-btn-cancel');
    this.$btnOk = this.$mask.find('.mi-btn-ok');
  };

  ModalInput.prototype._renderFields = function(){
    var html = '';
    var fields = this.options.fields;

    fields.forEach(function(f,i){
      html += '<div class="mi-field" data-index="' + i + '">' +
                '<label class="mi-label">' + (f.label || '') + '</label>';

      if (f.type === 'text') {
        html += '<input class="mi-input" type="text" value="' + (f.default||'') + '" placeholder="' + (f.placeholder||'') + '">';
      }

      if (f.type === 'textarea') {
        html += '<textarea class="mi-textarea" placeholder="' + (f.placeholder||'') + '">' + (f.default||'') + '</textarea>';
      }

      if (f.type === 'select') {
        html += `<select class="mi-select">`;
        // 👉 动态接口
        if (f.dataUrl) {
          $.ajax({
            url: f.dataUrl,
            method: f.method || "GET",
            data: f.params || {},
            dataType: "json",
            async: false,
            success: function(res){
              var list = res.data || [];
              list.forEach(item=>{
                var val = item[f.valueKey || "value"];
                var lab = item[f.labelKey || "label"];
                html += `<option value="${val}" ${val===f.default?"selected":""}>${lab}</option>`;
              });
            },
            error: function(){
              $select.html(`<option value="">加载失败</option>`);
            }
          });
        } else {
            f.options.forEach(o=>{
              html += `<option value="${o.value}" ${o.value===f.default?"selected":""}>${o.label}</option>`;
            });
        }
        html += `</select>`;
      }

      if (f.type === 'radio') {
        html += '<div class="mi-radio-group">';
        (f.options || []).forEach(function(o){
          html += '<label><input type="radio" name="mi_radio_' + i + '" value="' + o.value + '" ' + (o.value===f.default?'checked':'') + '> ' + o.label + '</label>';
        });
        html += '</div>';
      }

      html += '<div class="mi-error"></div></div>';
    });

    this.$fields.html(html);
  };

  ModalInput.prototype._bindEvents = function(){
    var self = this;

    this.$mask.on('click', function(e){
      if (e.target === self.$mask[0]) self.close();
    });

    this.$btnCancel.on('click', function(){ self.close(); });

    this.$btnOk.on('click', function(){
      var values = {};
      var valid = true;

      self.$fields.find('.mi-field').each(function(){
        var index = $(this).data('index');
        var f = self.options.fields[index];
        var $error = $(this).find('.mi-error');
        $error.hide();

        var value;
        if (f.type === 'text') value = $(this).find('input').val().trim();
        if (f.type === 'textarea') value = $(this).find('textarea').val().trim();
        if (f.type === 'select') value = $(this).find('select').val();
        if (f.type === 'radio') value = $(this).find('input[type=radio]:checked').val();

        if (f.validate) {
          var r = f.validate(value);
          if (!r.valid) {
            $error.text(r.msg || '输入有误').show();
            valid = false;
            return false;
          }
        }

        values[f.name] = value;
      });

      if (!valid) return;

      self.options.onConfirm(values);
      self.close();
    });

    $(document).on('keydown.modalInput', function(e){
      if (!self.$mask.hasClass('show')) return;
      if (e.key === 'Escape') self.close();
    });
  };

  ModalInput.prototype.open = function(){
    this.options.onOpen();
    this.$title.text(this.options.title);
    this.$btnCancel.text(this.options.cancelText);
    this.$btnOk.text(this.options.okText);
    this._renderFields();
    this.$mask.addClass('show');
  };

  ModalInput.prototype.close = function(){
    this.$mask.removeClass('show');
    this.options.onClose();
    this.$mask.remove();
  };

  // ===== 对外唯一入口 =====
  window.openModalInput = function(options){
    var modal = new ModalInput(options);
    modal.open();
    return modal;
  };

})(jQuery);

/* ===== 推荐样式（示例） =====
.mi-mask{position:fixed;inset:0;background:rgba(0,0,0,.45);display:flex;align-items:center;justify-content:center;z-index:10000;opacity:0;pointer-events:none}
.mi-mask.show{opacity:1;pointer-events:auto}
.mi-box{width:420px;background:#fff;border-radius:6px;overflow:hidden}
.mi-title{padding:12px 16px;font-weight:bold;border-bottom:1px solid #eee}
.mi-fields{padding:16px}
.mi-footer{padding:12px 16px;text-align:right;border-top:1px solid #eee}
.mi-error{color:#f00;font-size:12px;display:none}
*/