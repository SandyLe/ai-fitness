/*
 * jQuery 点击 div 生成下拉菜单插件（已修复 SyntaxError）
 * 用法：$(selector).dropdownMenu(options)
 */
;(function ($) {
  $.fn.dropdownMenu = function (options) {
    const settings = $.extend({
      menus: [],          // 菜单项 [{ text:'编辑', value:'edit', click: fn }]
      offsetX: 0,
      offsetY: 6
    }, options)

    // 关闭所有菜单
    function closeAll() {
      $('.jq-dropdown-menu').remove()
    }

    // 点击空白关闭（命名空间，防止重复绑定）
    $(document)
      .off('click.jqDropdown')
      .on('click.jqDropdown', function () {
        closeAll()
      })

    return this.each(function () {
      const $trigger = $(this)

      $trigger
        .off('click.jqDropdownItem')
        .on('click.jqDropdownItem', function (e) {
          e.stopPropagation()
          closeAll()

          const $menu = $('<div class="jq-dropdown-menu"></div>')

          settings.menus.forEach(function (item, index) {
            const $item = $('<div class="jq-dropdown-item"></div>')
              .text(item.text)
              .attr('data-value', item.value !== undefined ? item.value : item.text)

            $item.on('click', function (ev) {
              ev.stopPropagation()

              const value = $(this).data('value')
              const text = $(this).text()

              // 获取当前 div 内部的元素值
              let innerValue = null
              const $input = $trigger.find('input, textarea, select').first()
              if ($input.length) {
                innerValue = $input.val()
              } else {
                innerValue = $.trim($trigger.text())
              }

              if (typeof item.click === 'function') {
                item.click.call($trigger[0], value, text, index, innerValue)
              }

              closeAll()
            })

            $menu.append($item)
          })

          $('body').append($menu)

          const offset = $trigger.offset()
          const height = $trigger.outerHeight()

          $menu.css({
            left: offset.left + settings.offsetX,
            top: offset.top + height + settings.offsetY
          })
        })
    })
  }
})(jQuery)

/* ===== 建议样式 =====

.jq-dropdown-menu {
  position: absolute;
  min-width: 140px;
  background: #fff;
  border-radius: 6px;
  box-shadow: 0 8px 24px rgba(0,0,0,.15);
  padding: 6px 0;
  z-index: 9999;
}

.jq-dropdown-item {
  padding: 8px 14px;
  cursor: pointer;
  font-size: 14px;
}

.jq-dropdown-item:hover {
  background: #f5f7fa;
}
*/
