#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

with app.app_context():
    # 确保角色存在
    Role.insert_roles()

    # 创建测试用户
    user = User(
        email='test@example.com',
        username='testuser',
        password='password123',
        confirmed=True  # 跳过邮箱验证
    )

    db.session.add(user)
    db.session.commit()

    print(f"测试用户创建成功！")
    print(f"用户名: {user.username}")
    print(f"邮箱: {user.email}")
    print(f"密码: password123")
    print(f"已确认: {user.confirmed}")
