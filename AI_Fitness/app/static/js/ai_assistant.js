$(document).ready(function() {
  // 获取用户ID
  const userid = $('#userid').val();
  
  // 会话ID - 用于区分不同用户的请求
  const sessionId = generateSessionId();
  
  // 康训助手头像URL
  const botAvatarUrl = "/static/img/fitness_assistant.png"; // 康训助手头像路径
  
  // 自动调整文本区域高度
  function autoResizeTextarea() {
    const textarea = document.getElementById('input_text');
    textarea.style.height = 'auto';
    textarea.style.height = (textarea.scrollHeight) + 'px';
  }

  // 生成唯一的会话ID
  function generateSessionId() {
    return 'session_' + userid + '_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }

  // 获取用户信息
  function getUserInfo() {
    let username = "游客";
    let avatarUrl = "/static/img/visitor.jpg"; // 修正路径
    
    if (userid && userid !== "0") {
      // 如果用户已登录，使用用户ID作为用户名
      username = "用户" + userid;
      // 可以根据用户ID设置不同的头像
      avatarUrl = "/static/img/user.png"; // 修正路径
    }
    
    return { username, avatarUrl };
  }

  // 历史对话数据
  let chatHistory = [];
  
  // 当前对话ID
  let currentChatId = Date.now();
  
  // 加载历史对话
  function loadChatHistory() {
    // 从localStorage获取历史记录，使用用户ID作为key的一部分以区分不同用户
    const storageKey = userid !== '0' ? `chatHistory_${userid}` : 'chatHistory_guest';
    chatHistory = JSON.parse(localStorage.getItem(storageKey)) || [];
    
    // 如果没有历史记录，创建一个新的
    if (chatHistory.length === 0) {
      const newChat = {
        id: currentChatId,
        title: "新对话",
        timestamp: new Date().toISOString(),
        messages: []
      };
      chatHistory.push(newChat);
      saveChatHistory();
    } else {
      currentChatId = chatHistory[0].id;
    }
    
    renderChatHistory();
  }
  
  // 渲染历史对话列表
  function renderChatHistory() {
    const historyList = $('#historyList');
    historyList.empty();
    
    // 添加新建对话按钮
    const newChatButton = $(`
      <div class="history-item new-chat" id="newChatButton">
        <p><i class="fas fa-plus"></i> 新建对话</p>
      </div>
    `);
    
    historyList.append(newChatButton);
    
    // 添加历史对话
    chatHistory.forEach(chat => {
      const date = new Date(chat.timestamp);
      const formattedDate = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
      
      const historyItem = $(`
        <div class="history-item ${chat.id === currentChatId ? 'active' : ''}" data-id="${chat.id}">
          <p>${chat.title}</p>
          <div class="timestamp">${formattedDate}</div>
          <div class="delete-chat-btn" data-id="${chat.id}" title="删除此对话"><i class="fas fa-times"></i></div>
        </div>
      `);
      
      historyList.append(historyItem);
    });
    
    // 绑定点击事件
    $('.history-item:not(.new-chat)').click(function(e) {
      // 如果点击的是删除按钮，不执行加载对话操作
      if (!$(e.target).hasClass('delete-chat-btn') && !$(e.target).closest('.delete-chat-btn').length) {
        const chatId = parseInt($(this).data('id'));
        loadChat(chatId);
      }
    });
    
    // 绑定删除按钮点击事件
    $('.delete-chat-btn').click(function(e) {
      e.stopPropagation(); // 阻止事件冒泡
      const chatId = parseInt($(this).data('id'));
      deleteChat(chatId);
    });
    
    // 绑定新建对话按钮点击事件
    $('#newChatButton').click(createNewChat);
  }
  
  // 删除对话功能
  function deleteChat(chatId) {
    // 确认是否删除
    if (!confirm('确定要删除这个对话吗？')) {
      return;
    }
    
    // 查找要删除的对话索引
    const chatIndex = chatHistory.findIndex(c => c.id === chatId);
    if (chatIndex === -1) return;
    
    // 删除对话
    chatHistory.splice(chatIndex, 1);
    
    // 如果删除的是当前对话，加载第一个对话或创建新对话
    if (chatId === currentChatId) {
      if (chatHistory.length > 0) {
        loadChat(chatHistory[0].id);
      } else {
        createNewChat();
      }
    }
    
    // 保存并重新渲染
    saveChatHistory();
    renderChatHistory();
  }

  // 加载特定对话
  function loadChat(chatId) {
    currentChatId = chatId;
    
    // 更新活动状态
    $('.history-item').removeClass('active');
    $(`.history-item[data-id="${chatId}"]`).addClass('active');
    
    // 清空当前对话
    $('#conversation').empty();
    
    // 添加欢迎消息
    $('#conversation').append(`
      <div class="message-container">
        <div class="bot-avatar-container">
          <div class="avatar">
            <img src="${botAvatarUrl}" alt="康训助手" onerror="this.src='https://cdn-icons-png.flaticon.com/512/2936/2936886.png'">
          </div>
          <div class="username">康训助手</div>
        </div>
        <div class="bot-message">
          <div class="message-content">
            你好！我是你的康训智能助手。我可以帮你制定训练计划、解答康训疑问、提供饮食建议等。请告诉我你需要什么帮助？
          </div>
        </div>
      </div>
    `);
    
    // 加载对话消息
    const chat = chatHistory.find(c => c.id === chatId);
    if (chat && chat.messages.length > 0) {
      chat.messages.forEach(msg => {
        appendMessage(msg.role, msg.content);
      });
    }
    
    // 滚动到底部
    scrollToBottom();
  }
  
  // 保存历史对话
  function saveChatHistory() {
    const storageKey = userid !== '0' ? `chatHistory_${userid}` : 'chatHistory_guest';
    localStorage.setItem(storageKey, JSON.stringify(chatHistory));
  }
  
  // 创建新对话
  function createNewChat() {
    currentChatId = Date.now();
    const newChat = {
      id: currentChatId,
      title: "新对话",
      timestamp: new Date().toISOString(),
      messages: []
    };
    
    // 添加到历史记录的开头
    chatHistory.unshift(newChat);
    
    // 如果历史记录超过10条，删除最旧的
    if (chatHistory.length > 10) {
      chatHistory.pop();
    }
    
    saveChatHistory();
    loadChat(currentChatId);
    renderChatHistory();
  }
  
  // 更新对话标题
  function updateChatTitle(chatId, firstMessage) {
    const chat = chatHistory.find(c => c.id === chatId);
    if (chat) {
      // 使用用户的第一条消息作为标题，截取前20个字符
      chat.title = firstMessage.substring(0, 20) + (firstMessage.length > 20 ? '...' : '');
      saveChatHistory();
      renderChatHistory();
    }
  }
  
  // 添加消息到当前对话
  function addMessageToCurrentChat(role, content) {
    const chat = chatHistory.find(c => c.id === currentChatId);
    if (chat) {
      chat.messages.push({ role, content });
      
      // 如果是用户的第一条消息，更新对话标题
      if (role === 'user' && chat.messages.filter(m => m.role === 'user').length === 1) {
        updateChatTitle(currentChatId, content);
      }
      
      saveChatHistory();
    }
  }
  
  // 添加消息到对话框 - 修改这个函数
  function appendMessage(role, content) {
    const isUser = role === 'user';
    const formattedContent = content.replace(/\n/g, "<br>");
    
    if (isUser) {
      const userInfo = getUserInfo();
      const messageHtml = `
        <div class="message-container">
          <div class="user-message-header">
            <div class="username">${userInfo.username}</div>
            <div class="avatar">
              <img src="${userInfo.avatarUrl}" alt="用户头像" onerror="this.src='https://cdn-icons-png.flaticon.com/512/1077/1077114.png'">
            </div>
          </div>
          <div class="user-message">
            <div class="message-content">
              ${formattedContent}
            </div>
          </div>
        </div>
      `;
      
      $('#conversation').append(messageHtml);
    } else {
      const messageHtml = `
        <div class="message-container">
          <div class="bot-avatar-container">
            <div class="avatar">
              <img src="${botAvatarUrl}" alt="康训助手" onerror="this.src='https://cdn-icons-png.flaticon.com/512/2936/2936886.png'">
            </div>
            <div class="username">康训助手</div>
          </div>
          <div class="bot-message">
            <div class="message-content">
              ${formattedContent}
            </div>
          </div>
        </div>
      `;
      
      $('#conversation').append(messageHtml);
    }
    
    scrollToBottom();
  }
  
  // 滚动到对话底部
  function scrollToBottom() {
    const conversation = document.getElementById('conversation');
    conversation.scrollTop = conversation.scrollHeight;
  }
  
  // 发送消息到服务器
  function sendMessage(message) {
    $('#loading').show();
    console.log("发送消息到服务器:", message);
    console.log("使用会话ID:", sessionId);
    
    // 获取当前对话的历史记录
    const chat = chatHistory.find(c => c.id === currentChatId);
    let history = [];
    
    if (chat && chat.messages.length > 0) {
      // 只取最近的10条消息
      const recentMessages = chat.messages.slice(-10);
      history = recentMessages.map(msg => ({
        role: msg.role,
        content: msg.content
      }));
      console.log("发送历史对话:", history);
    }
    
    // 添加会话ID、用户ID和历史对话到请求中
    $.ajax({
      url: "/upload",
      type: "post",
      contentType: "application/json",
      dataType: 'json',
      data: JSON.stringify({ 
        input: message,
        session_id: sessionId,
        user_id: userid,
        history: history
      })
    }).done(function(response) {
      console.log("收到服务器响应:", response);
      const botResponse = response.msg;
      
      if (!botResponse) {
        console.error("服务器返回空响应");
        appendMessage('assistant', "抱歉，我暂时无法回答您的问题。请稍后再试。");
      } else {
        // 添加机器人回复到对话
        appendMessage('assistant', botResponse);
        addMessageToCurrentChat('assistant', botResponse);
      }
      
      $('#loading').hide();
    }).fail(function(error) {
      console.error("Error sending message:", error);
      appendMessage('assistant', "抱歉，发生了错误，请稍后再试。");
      $('#loading').hide();
    });
  }
  
  // 处理发送按钮点击
  $('#send_button').click(function() {
    const message = $('#input_text').val().trim();
    if (message) {
      // 添加用户消息到对话
      appendMessage('user', message);
      addMessageToCurrentChat('user', message);
      
      // 发送到服务器
      sendMessage(message);
      
      // 清空输入框
      $('#input_text').val('');
      $('#input_text').css('height', 'auto');
    }
  });
  
  // 处理回车键发送
  $('#input_text').keypress(function(e) {
    if (e.which === 13 && !e.shiftKey) {
      e.preventDefault();
      $('#send_button').click();
    }
  });
  
  // 自动调整文本区域高度
  $('#input_text').on('input', autoResizeTextarea);
  
  // 处理快捷提示点击
  $('.prompt-chip').click(function() {
    const promptText = $(this).data('prompt');
    $('#input_text').val(promptText);
    autoResizeTextarea();
  });
  
  // 添加到我的计划功能
  $('#add_to_plan_button').click(function() {
    // 获取当前对话中最后一条助手消息
    const chat = chatHistory.find(c => c.id === currentChatId);
    if (!chat || !chat.messages.length) {
      alert("当前没有可添加到计划的内容");
      return;
    }
    
    const assistantMessages = chat.messages.filter(m => m.role === 'assistant');
    if (!assistantMessages.length) {
      alert("当前没有可添加到计划的内容");
      return;
    }

    const lastAssistantMessage = assistantMessages[assistantMessages.length - 1].content;
    
    $("#loading").show();
    // 发送数据到服务器
    /*$.ajax({
      url: "/add-to-plan?id=" + userid,
      type: "post",
      contentType: "application/x-www-form-urlencoded",
      data: 'message=' + encodeURIComponent(lastAssistantMessage)
    }).done(function(response) {
      if (!response.success) {
        alert(response.error);
      } else if (response.success) {
        alert("已成功加入您的计划！");
      } else {
        alert("加入计划失败，请稍后重试！");
      }
      $("#loading").hide();
    }).fail(function() {
      alert("网络错误，请稍后重试！");
      $("#loading").hide();
    });*/
  });

  $("#add_to_plan_button").modalInput({
      title: "请给计划起个名吧",
      animation: "zoom", // fade / zoom / slide

      fields: [
        {
          type: "text",
          name: "title",
          label: "计划名称",
          placeholder: "请输入计划名称",
          validate: v => v ? {valid:true} : {valid:false, msg:"计划名称不能为空"}
        },
        /*{
          type: "textarea",
          name: "desc",
          label: "描述",
          placeholder: "请输入描述内容",
          default: "",
          validate: v => ({valid:true})
        },
        {
          type: "select",
          name: "category",
          label: "类别",
          default: "sport",
          options: [
            {value:"sport", label:"运动"},
            {value:"diet",  label:"饮食"},
            {value:"rest",  label:"休息"}
          ]
        },
        {
          type: "radio",
          name: "level",
          label: "强度等级",
          default: "middle",
          options: [
            {value:"low", label:"低"},
            {value:"middle", label:"中"},
            {value:"high", label:"高"},
          ]
        }*/
      ],

      onConfirm: function(values){
//        alert("提交的数据：" + JSON.stringify(values, null, 2));
        submitPlan(values.title);
      }
    });

  function submitPlan(title) {
      // 获取当前对话中最后一条助手消息
        const chat = chatHistory.find(c => c.id === currentChatId);
        if (!chat || !chat.messages.length) {
          alert("当前没有可添加到计划的内容");
          return;
        }

        const assistantMessages = chat.messages.filter(m => m.role === 'assistant');
        if (!assistantMessages.length) {
          alert("当前没有可添加到计划的内容");
          return;
        }

        const lastAssistantMessage = assistantMessages[assistantMessages.length - 1].content;

        $("#loading").show();
        // 发送数据到服务器
        $.ajax({
          url: "/add-to-plan?id=" + userid,
          type: "post",
          contentType: "application/x-www-form-urlencoded",
          data: 'message=' + encodeURIComponent(lastAssistantMessage) + '&title=' + title
        }).done(function(response) {
          if (!response.success) {
            alert(response.error);
          } else if (response.success) {
            alert("已成功加入您的计划！");
          } else {
            alert("加入计划失败，请稍后重试！");
          }
          $("#loading").hide();
        }).fail(function() {
          alert("网络错误，请稍后重试！");
          $("#loading").hide();
        });
    }
  // 初始化
  loadChatHistory();
});