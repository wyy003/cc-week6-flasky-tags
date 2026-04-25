#!/usr/bin/env python
"""
Week 6 Day 3 - 测试标签管理功能
"""
import os
from app import create_app, db
from app.models import Post, Tag, User

def test_tag_management():
    """测试标签管理功能"""
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')

    with app.app_context():
        print("=" * 60)
        print("Week 6 Day 3 - 标签管理功能测试")
        print("=" * 60)

        # 1. 创建一些测试标签
        print("\n1. 创建测试标签...")
        test_tag1 = Tag(name='unused-tag-1')
        test_tag2 = Tag(name='unused-tag-2')
        test_tag3 = Tag(name='used-tag')

        db.session.add_all([test_tag1, test_tag2, test_tag3])
        db.session.commit()

        print(f"   创建了 3 个标签: {test_tag1.name}, {test_tag2.name}, {test_tag3.name}")

        # 2. 给一个标签关联文章
        print("\n2. 关联标签到文章...")
        user = User.query.first()
        if user:
            post = Post(body="Test post with tag", author=user)
            post.tags.append(test_tag3)
            db.session.add(post)
            db.session.commit()
            print(f"   文章已关联标签: {test_tag3.name}")
        else:
            print("   ⚠️  没有找到用户，跳过文章创建")

        # 3. 测试 get_all_tags_with_count
        print("\n3. 测试 get_all_tags_with_count()...")
        all_tags = Tag.get_all_tags_with_count()
        print(f"   总标签数: {len(all_tags)}")
        for tag, count in all_tags:
            print(f"   - {tag.name}: {count} 篇文章")

        # 4. 测试 post_count 属性
        print("\n4. 测试 Tag.post_count 属性...")
        for tag in [test_tag1, test_tag2, test_tag3]:
            print(f"   {tag.name}: {tag.post_count} 篇文章")

        # 5. 测试清理未使用的标签
        print("\n5. 测试 cleanup_unused_tags()...")
        unused_count_before = len([t for t, c in Tag.get_all_tags_with_count() if c == 0])
        print(f"   清理前未使用标签数: {unused_count_before}")

        cleaned = Tag.cleanup_unused_tags()
        print(f"   清理了 {cleaned} 个未使用的标签")

        unused_count_after = len([t for t, c in Tag.get_all_tags_with_count() if c == 0])
        print(f"   清理后未使用标签数: {unused_count_after}")

        # 6. 验证清理结果
        print("\n6. 验证清理结果...")
        remaining_tags = Tag.get_all_tags_with_count()
        print(f"   剩余标签数: {len(remaining_tags)}")

        all_have_posts = all(count > 0 for _, count in remaining_tags)
        if all_have_posts:
            print("   ✅ 所有剩余标签都有关联文章")
        else:
            print("   ❌ 仍有未使用的标签")

        # 7. 测试删除特定标签
        print("\n7. 测试删除特定标签...")
        if remaining_tags:
            tag_to_delete = remaining_tags[0][0]
            tag_name = tag_to_delete.name
            print(f"   删除标签: {tag_name}")

            db.session.delete(tag_to_delete)
            db.session.commit()

            # 验证删除
            deleted_tag = Tag.query.filter_by(name=tag_name).first()
            if deleted_tag is None:
                print(f"   ✅ 标签 '{tag_name}' 已成功删除")
            else:
                print(f"   ❌ 标签 '{tag_name}' 删除失败")

        print("\n" + "=" * 60)
        print("标签管理功能测试完成")
        print("=" * 60)

if __name__ == '__main__':
    test_tag_management()
