#!/usr/bin/env python
"""
标签系统业务验证脚本

测试：
1. 创建标签
2. 给文章添加标签
3. 查询文章的标签
4. 查询热门标签
"""
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models import Post, Tag, User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

with app.app_context():
    print("=== 标签系统业务验证 ===\n")

    # 1. 获取测试用户和文章
    user = User.query.filter_by(username='testuser').first()
    if not user:
        print("❌ 找不到测试用户")
        sys.exit(1)

    # 创建一篇测试文章
    post = Post(body="这是一篇测试文章，用于验证标签功能", author=user)
    db.session.add(post)
    db.session.commit()
    print(f"✅ 创建测试文章 ID: {post.id}")

    # 2. 创建标签
    tag1 = Tag.get_or_create('python')
    tag2 = Tag.get_or_create('flask')
    tag3 = Tag.get_or_create('web开发')
    db.session.commit()
    print(f"✅ 创建标签: python, flask, web开发")

    # 3. 给文章添加标签
    post.tags.append(tag1)
    post.tags.append(tag2)
    post.tags.append(tag3)
    db.session.commit()
    print(f"✅ 给文章 {post.id} 添加了 3 个标签")

    # 4. 查询文章的所有标签
    print(f"\n文章 {post.id} 的标签:")
    for tag in post.tags:
        print(f"  - {tag.name}")

    # 5. 查询某个标签下的所有文章
    python_tag = Tag.query.filter_by(name='python').first()
    print(f"\n标签 'python' 下的文章:")
    for p in python_tag.posts:
        print(f"  - 文章 ID {p.id}: {p.body[:30]}...")

    # 6. 测试热门标签（需要更多数据才有意义）
    print(f"\n热门标签 Top 5:")
    popular = Tag.get_popular_tags(5)
    for tag, count in popular:
        print(f"  - {tag.name}: {count} 篇文章")

    print("\n=== 验证完成 ===")
    print("标签存储功能正常工作！")
