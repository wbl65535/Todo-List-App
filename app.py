import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 创建Flask应用实例
app = Flask(__name__)

# 配置数据库 - 适配不同环境
if os.environ.get('VERCEL'):
    # Vercel环境使用内存数据库（仅作演示，实际部署需要外部数据库）
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
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

# 添加待办事项
@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    description = request.form.get('description', '')
    
    if title:
        new_todo = Todo(title=title, description=description)
        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return '添加事项时出错'
    else:
        return redirect(url_for('index'))

# 更新待办事项状态
@app.route('/update/<int:id>')
def update(id):
    todo = Todo.query.get_or_404(id)
    todo.completed = not todo.completed
    try:
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return '更新状态时出错'

# 删除待办事项
@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    try:
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return '删除事项时出错'

# 编辑待办事项页面
@app.route('/edit/<int:id>')
def edit(id):
    todo = Todo.query.get_or_404(id)
    return render_template('edit.html', todo=todo)

# 保存编辑后的待办事项
@app.route('/save/<int:id>', methods=['POST'])
def save(id):
    todo = Todo.query.get_or_404(id)
    todo.title = request.form['title']
    todo.description = request.form['description']
    
    try:
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return '保存事项时出错'

if __name__ == '__main__':
    app.run(debug=True)