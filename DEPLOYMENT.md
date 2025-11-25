# 部署指南

本文档介绍了如何将Todo List应用部署到服务器上。

## 本地部署

### 1. 环境要求
- Python 3.7 或更高版本
- pip 包管理器

### 2. 安装步骤

1. 克隆或下载项目代码：
   ```
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
   ```
   pip install -r requirements.txt
   ```

4. 运行应用：
   ```
   python app.py
   ```

5. 访问应用：
   打开浏览器访问 `http://localhost:5000`

## 生产环境部署

### 使用Gunicorn部署（推荐）

1. 安装Gunicorn：
   ```
   pip install gunicorn
   ```

2. 运行应用：
   ```
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

### 使用Docker部署

1. 创建Dockerfile：
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 5000
   
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
   ```

2. 构建镜像：
   ```
   docker build -t todo-app .
   ```

3. 运行容器：
   ```
   docker run -p 5000:5000 todo-app
   ```

## 配置说明

### 数据库配置
应用默认使用SQLite数据库，数据存储在 `todo.db` 文件中。如需修改数据库配置，请修改 `app.py` 中的以下行：
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
```

### 环境变量
可以使用以下环境变量来配置应用：

- `FLASK_ENV`: 设置为 `production` 以启用生产模式
- `SECRET_KEY`: Flask应用的密钥（生产环境必需）

## 故障排除

### 常见问题

1. ** ImportError: No module named flask **
   解决方案：确保已安装所有依赖项：
   ```
   pip install -r requirements.txt
   ```

2. ** PermissionError: [Errno 13] Permission denied: 'todo.db' **
   解决方案：检查应用对当前目录的写入权限。

3. ** 应用启动后无法访问 **
   解决方案：检查防火墙设置，确保相应端口已开放。

## 性能优化建议

1. 使用反向代理（如Nginx）处理静态文件
2. 配置适当的日志记录
3. 定期备份数据库文件
4. 在生产环境中关闭调试模式（debug=False）