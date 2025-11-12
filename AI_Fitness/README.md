# AI-Fitness 智能康训助手

## 项目简介

AI-Fitness是一个智能康训助手应用，旨在通过人工智能技术帮助用户进行康训训练。该应用能够识别用户的运动姿势，提供实时反馈，并根据用户的康训水平和目标提供个性化的训练计划。

## 功能特点

- **姿势识别与纠正**：通过摄像头实时分析用户的运动姿势，提供纠正建议
- **个性化训练计划**：根据用户的康训水平、目标和偏好生成定制化的训练计划
- **实时反馈**：在训练过程中提供即时反馈和指导
- **训练数据分析**：记录和分析用户的训练数据，展示进步情况
- **多种训练模式**：支持多种康训训练模式，满足不同用户的需求
- **AI智能助手**：提供康训知识咨询和训练建议
- **社区交流**：用户可以在社区分享康训经验，交流心得
- **个人中心**：管理个人信息、查看训练历史和统计数据

## 技术架构

### 前端技术
- HTML5/CSS3/JavaScript
- Vue.js（根据用户偏好）
- Bootstrap

### 后端技术
- Python 3.8+
- Flask Web框架
- MySQL数据库

### AI技术
- MediaPipe（姿势识别）
- 讯飞星火大模型（智能助手）

### 部署环境
- Docker容器化部署
- Nginx反向代理

## 目录结构

```
AI-fitness/
├── app/                    # 应用主目录
│   ├── __init__.py         # 应用初始化
│   ├── config.py           # 配置文件
│   ├── utils.py            # 工具函数
│   ├── config/             # 配置目录
│   │   └── fitness/        # 康训相关配置
│   │   └── datajson/       # 康训数据JSON文件
│   ├── routes/             # 路由目录
│   │   ├── auth.py         # 认证路由
│   │   ├── ai_assistant.py # AI助手路由
│   │   ├── community.py    # 社区路由
│   │   └── fitness.py      # 康训路由
│   ├── services/           # 服务层
│   │   ├── aiApi.py        # AI API服务
│   │   ├── basefunc.py     # 基础功能服务
│   │   ├── ai_service.py   # AI服务
│   │   ├── db_service.py   # 数据库服务
│   │   └── db_services/    # 数据库服务模块
│   │       ├── user_info.py      # 用户信息服务
│   │       ├── user_date.py      # 用户训练数据服务
│   │       ├── user_discussion.py# 用户讨论服务
│   │       ├── user_plan.py      # 用户计划服务
│   │       └── ...               # 其他数据库服务
│   ├── static/             # 静态资源
│   │   ├── css/            # 样式文件
│   │   ├── js/             # JavaScript文件
│   │   └── pose_fitness_js/ # 姿势识别JS文件
│   ├── templates/          # 模板文件
│   │   ├── auth/           # 认证相关页面
│   │   ├── ai_assistant/   # AI助手页面
│   │   ├── community/      # 社区页面
│   │   ├── fitness/        # 康训相关页面
│   │   ├── bmi/            # BMI计算页面
│   │   └── includes/       # 公共页面组件
│   └── utils/              # 工具模块
│       ├── libmysql.py     # MySQL数据库操作封装
│       ├── result_type.py  # 响应类型定义
│       └── user_info.py    # 用户信息处理
├── AI-Fitness-modle-code/  # AI模型代码
├── tests/                  # 测试目录
├── run.py                  # 应用启动脚本
├── run_tests.py            # 测试运行脚本
├── work_out.sql            # 数据库初始化脚本
├── Dockerfile              # Docker配置文件
└── requirements.txt        # Python依赖包
```

## 核心功能模块

### 1. 用户认证系统
- 用户注册/登录
- 个人信息管理
- 密码修改

### 2. 康训训练系统
- 肌肉群训练（胸肌、背肌、腿部等）
- 器材选择（哑铃、徒手）
- 姿势识别与分析
- 训练报告生成

### 3. AI智能助手
- 康训知识问答
- 训练建议
- 营养指导

### 4. 社区交流
- 发布讨论
- 查看他人分享
- 搜索功能

### 5. 数据统计
- 训练历史记录
- 训练效果分析
- 个人数据统计

## 数据库设计

系统使用MySQL数据库，主要包含以下表：

1. `user_info` - 用户信息表
2. `user_date` - 用户训练数据表
3. `user_discussion` - 用户讨论表
4. `user_plan` - 用户计划表
5. `user_clock` - 用户打卡表
6. `user_mapping` - 用户关联表
7. `user_topic` - 用户话题表

详细表结构请参考 [work_out.sql](file:///d%3A/myItem/%E6%99%BA%E8%83%BD%E5%81%A5%E8%BA%AB%E8%BE%85%E5%8A%A9%E7%B3%BB%E7%BB%9F/AI_Fitness/work_out.sql) 文件。

## 配置说明

详细的配置说明请查看 [CONFIGURATION.md](file:///d%3A/myItem/%E6%99%BA%E8%83%BD%E5%81%A5%E8%BA%AB%E8%BE%85%E5%8A%A9%E7%B3%BB%E7%BB%9F/AI_Fitness/CONFIGURATION.md) 文件，包含数据库配置、AI API配置等。

## 安装指南

### 前提条件

- Python (v3.8+)
- MySQL (v5.7+)
- Node.js (v14.0+) (如果需要)

### 安装步骤

1. 克隆仓库
   ```bash
   git clone https://github.com/yourusername/AI-fitness.git
   cd AI-fitness
   ```

2. 安装Python依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 配置数据库
   - 创建MySQL数据库
   - 执行 [work_out.sql](file:///d%3A/myItem/%E6%99%BA%E8%83%BD%E5%81%A5%E8%BA%AB%E8%BE%85%E5%8A%A9%E7%B3%BB%E7%BB%9F/AI_Fitness/work_out.sql) 初始化表结构
   - 复制 [app/config_example.py](file:///d%3A/myItem/%E6%99%BA%E8%83%BD%E5%81%A5%E8%BA%AB%E8%BE%85%E5%8A%A9%E7%B3%BB%E7%BB%9F/AI_Fitness/app/config_example.py) 为 `app/config.py` 并修改其中的数据库配置
   - 或者直接修改 [app/config.py](file:///d%3A/myItem/%E6%99%BA%E8%83%BD%E5%81%A5%E8%BA%AB%E8%BE%85%E5%8A%A9%E7%B3%BB%E7%BB%9F/AI_Fitness/app/config.py) 中的配置信息（注意：该文件已被.gitignore忽略，不会被提交到仓库）

4. 配置AI API（可选）
   - 申请讯飞星火API密钥（https://www.xfyun.cn/）
   - 修改 [app/config.py](file:///d%3A/myItem/%E6%99%BA%E8%83%BD%E5%81%A5%E8%BA%AB%E8%BE%85%E5%8A%A9%E7%B3%BB%E7%BB%9F/AI_Fitness/app/config.py) 中的AI API配置

5. 启动应用
   ```bash
   python run.py
   ```

6. 访问应用
   打开浏览器访问 `http://localhost:1005`

## Docker部署

项目提供了Dockerfile用于容器化部署：

```
# 构建镜像
docker build -t ai-fitness .

# 运行容器
docker run -p 1005:1005 ai-fitness
```

## API接口说明

### 认证相关接口
- `POST /login` - 用户登录
- `POST /register` - 用户注册
- `GET /logout` - 用户登出

### 康训相关接口
- `GET /fitness/start` - 开始训练
- `GET /fitness/<muscle>/<gender>/<equipment>` - 肌肉训练
- `GET /fitness/get_report` - 获取训练报告
- `POST /fitness/save_report` - 保存训练报告

### AI助手接口
- `GET /ai_assistant/` - AI助手页面

### 社区接口
- `GET /community/` - 社区主页
- `GET /community/create` - 创建讨论
- `POST /community/save_discussion` - 保存讨论

## 贡献指南

欢迎贡献代码和建议！

1. Fork本项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

详细信息请查看[CONTRIBUTING.md](CONTRIBUTING.md)和我们的[行为准则](CODE_OF_CONDUCT.md)。

## 安全说明

为了保护敏感信息，项目采用了以下安全措施：

1. `app/config.py` 文件已被添加到 [.gitignore](file:///d%3A/myItem/%E6%99%BA%E8%83%BD%E5%81%A5%E8%BA%AB%E8%BE%85%E5%8A%A9%E7%B3%BB%E7%BB%9F/AI_Fitness/.gitignore) 文件中，不会被提交到Git仓库
2. 项目中提供了 [app/config_example.py](file:///d%3A/myItem/%E6%99%BA%E8%83%BD%E5%81%A5%E8%BA%AB%E8%BE%85%E5%8A%A9%E7%B3%BB%E7%BB%9F/AI_Fitness/app/config_example.py) 作为配置文件的示例
3. SECRET_KEY 会优先从环境变量中获取，如果没有则自动生成

在生产环境中，请务必：
- 将配置信息存储在环境变量中
- 使用强密码
- 定期更新密钥和密码

## 许可证

本项目采用 MIT 许可证。请查看[LICENSE](LICENSE)文件以获取更多信息。

### MIT许可证简要说明

MIT许可证是一个宽松的开源许可证，允许：

- 商业使用
- 修改代码
- 分发源代码或二进制文件
- 专利使用
- 私人使用

限制条件：

- 必须包含原始版权声明和许可证文本

无担保：

- 软件按"现状"提供，不提供任何形式的担保
