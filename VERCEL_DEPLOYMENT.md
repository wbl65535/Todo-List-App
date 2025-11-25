# Vercel 部署指南

本文档介绍了如何将 Todo List 应用部署到 Vercel 平台。

## 部署步骤

### 1. 准备工作
1. 确保项目已推送到 GitHub、GitLab 或 Bitbucket 仓库
2. 注册并登录 [Vercel](https://vercel.com) 账号

### 2. 连接仓库
1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 点击 "New Project"
3. 选择包含此项目的 Git 仓库
4. 点击 "Import"

### 3. 配置项目
Vercel 会自动检测这是一个 Python 项目，并使用 `vercel.json` 文件中的配置：

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python",
      "config": {
        "runtime": "python3.9",
        "maxLambdaSize": "15mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### 4. 环境变量设置
由于 Vercel 是无服务器环境，我们需要对应用进行一些调整以适应其环境：

1. 在 Vercel 项目的 "Settings" → "Environment Variables" 中添加以下环境变量：
   ```
   FLASK_ENV=production
   ```

### 5. 部署限制说明
需要注意的是，Vercel 的 serverless 环境有一些限制：

1. **文件系统访问**：Vercel 的 serverless 函数是只读的，除了 `/tmp` 目录。SQLite 数据库文件不能在每次请求时持久化保存。

2. **解决方案**：
   - 使用 Vercel 的 PostgreSQL 数据库插件
   - 使用外部数据库服务（如 MongoDB Atlas, Firebase 等）
   - 将数据存储在外部服务中

## 适配 Vercel 的代码修改

为了使应用在 Vercel 上正常运行，需要对 `app.py` 进行以下修改：

1. 修改数据库路径以适应 Vercel 环境
2. 添加 Vercel 特定的配置

### 修改后的 app.py 示例：

```python
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 创建Flask应用实例
app = Flask(__name__)

# 配置数据库 - 适配 Vercel 环境
if os.environ.get('VERCEL'):
    # Vercel 环境使用 PostgreSQL 或其他外部数据库
    # 这里只是一个示例，实际部署时需要配置真实的数据库连接
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///:memory:')
else:
    # 本地开发环境
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)

# 定义待办事项模型
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Todo {self.title}>'

# 创建数据库表
with app.app_context():
    db.create_all()

# 主页路由 - 显示所有待办事项
@app.route('/')
def index():
    todos = Todo.query.order_by(Todo.created_date.desc()).all()
    return render_template('index.html', todos=todos)

# 其他路由保持不变...
```

## 替代方案

如果需要完整的 SQLite 支持，建议考虑以下替代部署方案：

1. **Heroku**：对 Python Flask 应用支持更好
2. **Railway**：类似 Vercel 但对传统 Web 应用支持更好
3. **PythonAnywhere**：专门针对 Python 应用的托管服务

## 获取帮助

如果在部署过程中遇到问题，可以参考：

1. [Vercel Python 文档](https://vercel.com/docs/runtimes#official-runtimes/python)
2. [Vercel Serverless Functions 文档](https://vercel.com/docs/serverless-functions/introduction)