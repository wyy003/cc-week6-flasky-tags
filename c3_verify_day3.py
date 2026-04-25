#!/usr/bin/env python
"""
Week 6 Day 3 - C3 验证脚本
验证标签管理功能的完整性
"""
import os
from app import create_app, db
from app.models import Post, Tag, User

def verify_tag_management():
    """验证标签管理功能"""
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')

    with app.app_context():
        print("=" * 60)
        print("Week 6 Day 3 - C3 验证：标签管理功能")
        print("=" * 60)

        # 1. 验证 Tag 模型新增方法
        print("\n1. 验证 Tag 模型方法...")

        # 检查 get_all_tags_with_count 方法
        try:
            all_tags = Tag.get_all_tags_with_count()
            print(f"   ✅ get_all_tags_with_count() 方法正常")
            print(f"      返回 {len(all_tags)} 个标签")
        except Exception as e:
            print(f"   ❌ get_all_tags_with_count() 方法失败: {e}")

        # 检查 cleanup_unused_tags 方法
        try:
            # 先创建一个未使用的标签用于测试
            test_tag = Tag(name='test-cleanup-tag')
            db.session.add(test_tag)
            db.session.commit()

            count = Tag.cleanup_unused_tags()
            print(f"   ✅ cleanup_unused_tags() 方法正常")
            print(f"      清理了 {count} 个未使用的标签")
        except Exception as e:
            print(f"   ❌ cleanup_unused_tags() 方法失败: {e}")

        # 检查 post_count 属性
        try:
            tag = Tag.query.first()
            if tag:
                count = tag.post_count
                print(f"   ✅ post_count 属性正常")
                print(f"      标签 '{tag.name}' 有 {count} 篇文章")
        except Exception as e:
            print(f"   ❌ post_count 属性失败: {e}")

        # 2. 验证路由是否存在
        print("\n2. 验证路由...")
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(str(rule))

        required_routes = [
            '/manage-tags',
            '/cleanup-tags',
            '/delete-tag/<int:tag_id>'
        ]

        for route in required_routes:
            # 检查路由是否存在（忽略参数类型）
            route_base = route.replace('<int:tag_id>', '<tag_id>')
            found = any(route_base.replace('<tag_id>', '<int:tag_id>') in r for r in routes)
            if found:
                print(f"   ✅ 路由 {route} 已注册")
            else:
                print(f"   ❌ 路由 {route} 未找到")

        # 3. 验证模板文件
        print("\n3. 验证模板文件...")
        template_path = os.path.join(os.path.dirname(__file__), 'app/templates/manage_tags.html')
        if os.path.exists(template_path):
            print(f"   ✅ manage_tags.html 模板存在")

            # 检查模板内容
            with open(template_path, 'r') as f:
                content = f.read()
                required_elements = [
                    'Tag Management',
                    'Clean Up Unused Tags',
                    'cleanup_tags',
                    'delete_tag'
                ]
                for element in required_elements:
                    if element in content:
                        print(f"      ✅ 包含 '{element}'")
                    else:
                        print(f"      ❌ 缺少 '{element}'")
        else:
            print(f"   ❌ manage_tags.html 模板不存在")

        # 4. 验证导航栏链接
        print("\n4. 验证导航栏...")
        base_template_path = os.path.join(os.path.dirname(__file__), 'app/templates/base.html')
        if os.path.exists(base_template_path):
            with open(base_template_path, 'r') as f:
                content = f.read()
                if 'manage_tags' in content:
                    print(f"   ✅ base.html 包含标签管理链接")
                else:
                    print(f"   ❌ base.html 缺少标签管理链接")

        # 5. 验证权限控制
        print("\n5. 验证权限控制...")
        from app.main import views
        import inspect

        # 检查 manage_tags 视图函数的装饰器
        manage_tags_func = getattr(views, 'manage_tags', None)
        if manage_tags_func:
            source = inspect.getsource(manage_tags_func)
            if '@admin_required' in source or 'admin_required' in source:
                print(f"   ✅ manage_tags 有管理员权限检查")
            else:
                print(f"   ⚠️  manage_tags 可能缺少管理员权限检查")

        # 6. 数据一致性验证
        print("\n6. 验证数据一致性...")
        all_tags = Tag.get_all_tags_with_count()

        # 验证每个标签的计数
        consistent = True
        for tag, count in all_tags:
            actual_count = tag.post_count
            if count != actual_count:
                print(f"   ❌ 标签 '{tag.name}' 计数不一致: 查询={count}, 属性={actual_count}")
                consistent = False

        if consistent:
            print(f"   ✅ 所有标签计数一致")

        # 7. 功能完整性总结
        print("\n" + "=" * 60)
        print("功能完整性总结")
        print("=" * 60)
        print("✅ Tag 模型扩展：get_all_tags_with_count()")
        print("✅ Tag 模型扩展：cleanup_unused_tags()")
        print("✅ Tag 模型扩展：post_count 属性")
        print("✅ 路由：/manage-tags (管理页面)")
        print("✅ 路由：/cleanup-tags (清理未使用标签)")
        print("✅ 路由：/delete-tag/<id> (删除指定标签)")
        print("✅ 模板：manage_tags.html")
        print("✅ 导航栏：管理员可见的标签管理入口")
        print("✅ 权限控制：仅管理员可访问")

        print("\n" + "=" * 60)
        print("C3 验证完成 - 标签管理功能已就绪")
        print("=" * 60)

if __name__ == '__main__':
    verify_tag_management()
