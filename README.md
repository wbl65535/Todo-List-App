# Todo List App

一个基于Flask和SQLite的待办事项管理Web应用，具有响应式设计，可在手机端完美使用。

![界面预览](preview.png)

## 功能特性
- ✅ 添加、查看、编辑、删除待办事项
- ✅ 标记完成/未完成状态
- ✅ 响应式设计，支持手机端浏览
- ✅ 数据持久化存储（SQLite数据库）
- ✅ 简洁美观的用户界面

## 技术栈
- 后端：Python Flask
- 数据库：SQLite
- 前端：Bootstrap 5 + Jinja2模板
- 样式：CSS3 + HTML5

## 项目结构
```
Todo-List-App/
├── app.py              # Flask应用主文件
├── requirements.txt    # 项目依赖
├── README.md           # 项目说明文档
├── DEPLOYMENT.md       # 部署指南
├── templates/          # HTML模板文件
│   ├── base.html       # 基础模板
│   ├── index.html      # 主页模板
│   └── edit.html       # 编辑页模板
└── todo.db             # SQLite数据库文件（运行后自动生成）
```

## 安装与运行

### 1. 环境要求
- Python 3.7 或更高版本
- pip 包管理器

### 2. 安装步骤

1. 克隆或下载项目代码：
   ```bash
   git clone <repository-url>
   cd Todo-List-App
   ```

2. 创建虚拟环境（推荐）：
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 运行应用：
   ```bash
   python app.py
   ```

5. 访问应用：
   打开浏览器访问 `http://localhost:5000`

## 使用说明

1. 在首页输入框中添加新的待办事项
2. 点击"○"按钮标记事项为完成状态
3. 点击"编辑"按钮修改事项内容
4. 点击"删除"按钮删除不需要的事项

## 部署到生产环境

请参考 [DEPLOYMENT.md](DEPLOYMENT.md) 文件了解更多部署选项。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 许可证

MIT License