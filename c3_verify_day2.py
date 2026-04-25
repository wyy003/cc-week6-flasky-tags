#!/usr/bin/env python
"""
Week 6 Day 2 - C3 验证脚本
验证标签系统的数据准确性
"""
import os
from app import create_app, db
from app.models import Post, Tag, post_tags
from sqlalchemy import func

def verify_tag_system():
    """验证标签系统数据准确性"""
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')

    with app.app_context():
        print("=" * 60)
        print("Week 6 Day 2 - C3 验证：标签系统数据准确性")
        print("=" * 60)

        # 1. 验证标签总数
        total_tags = Tag.query.count()
        print(f"\n1. 标签总数: {total_tags}")

        # 2. 验证文章-标签关联总数
        total_associations = db.session.query(post_tags).count()
        print(f"2. 文章-标签关联总数: {total_associations}")

        # 3. 列出所有标签及其使用次数
        print("\n3. 所有标签及使用次数:")
        tags_with_count = db.session.query(
            Tag.name,
            func.count(post_tags.c.post_id).label('count')
        ).outerjoin(post_tags).group_by(Tag.id).order_by(
            func.count(post_tags.c.post_id).desc()
        ).all()

        for tag_name, count in tags_with_count:
            print(f"   - {tag_name}: {count} 篇文章")

        # 4. 随机抽取一篇有标签的文章验证
        print("\n4. 随机抽取文章验证标签关联:")
        post_with_tags = Post.query.filter(Post.tags.any()).first()

        if post_with_tags:
            print(f"   文章标题: {post_with_tags.body[:50]}...")
            print(f"   文章 ID: {post_with_tags.id}")
            print(f"   关联标签: {[tag.name for tag in post_with_tags.tags]}")

            # 手动验证数据库中的关联
            manual_check = db.session.query(Tag.name).join(
                post_tags
            ).filter(
                post_tags.c.post_id == post_with_tags.id
            ).all()

            manual_tags = [name for (name,) in manual_check]
            print(f"   数据库直接查询: {manual_tags}")

            # 验证一致性
            orm_tags = sorted([tag.name for tag in post_with_tags.tags])
            db_tags = sorted(manual_tags)

            if orm_tags == db_tags:
                print("   ✅ ORM 查询与数据库查询一致")
            else:
                print("   ❌ 数据不一致！")
                print(f"      ORM: {orm_tags}")
                print(f"      DB:  {db_tags}")
        else:
            print("   ⚠️  没有找到带标签的文章")

        # 5. 验证热门标签计算
        print("\n5. 验证热门标签（Top 5）:")
        popular_tags = db.session.query(
            Tag.name,
            func.count(post_tags.c.post_id).label('count')
        ).join(post_tags).group_by(Tag.id).order_by(
            func.count(post_tags.c.post_id).desc()
        ).limit(5).all()

        for idx, (tag_name, count) in enumerate(popular_tags, 1):
            print(f"   {idx}. {tag_name}: {count} 次")

        # 6. 验证标签筛选功能
        print("\n6. 验证标签筛选功能:")
        if popular_tags:
            test_tag_name = popular_tags[0][0]
            test_tag = Tag.query.filter_by(name=test_tag_name).first()

            if test_tag:
                filtered_posts = Post.query.filter(
                    Post.tags.contains(test_tag)
                ).count()

                print(f"   测试标签: {test_tag_name}")
                print(f"   筛选结果: {filtered_posts} 篇文章")
                print(f"   预期数量: {popular_tags[0][1]} 篇")

                if filtered_posts == popular_tags[0][1]:
                    print("   ✅ 筛选功能正确")
                else:
                    print("   ❌ 筛选结果不匹配！")

        print("\n" + "=" * 60)
        print("C3 验证完成")
        print("=" * 60)

if __name__ == '__main__':
    verify_tag_system()
