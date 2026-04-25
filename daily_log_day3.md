# Week 6 Day 3 协作日志

## 日期
2026-04-25

## 今天完成的工作

### 1. 标签管理功能实现 ✅

#### 后端功能
- **Tag 模型扩展**：
  - `get_all_tags_with_count()`: 获取所有标签及其使用次数
  - `cleanup_unused_tags()`: 自动清理未使用的标签
  - `post_count` 属性: 获取标签关联的文章数量

#### 路由和视图
- `/manage-tags`: 标签管理页面（仅管理员）
- `/cleanup-tags`: 批量清理未使用标签
- `/delete-tag/<id>`: 删除指定标签

#### 前端界面
- 标签管理页面 (`manage_tags.html`)
  - 显示所有标签及使用次数
  - 显示标签创建时间
  - 一键清理未使用标签按钮
  - 单个标签删除按钮
  - 统计信息面板
- 导航栏添加"Manage Tags"入口（仅管理员可见）

### 2. 权限控制
- 使用 `@admin_required` 装饰器
- 仅管理员可以访问标签管理功能
- 非管理员访问会重定向到登录页

### 3. 测试验证
- 创建了 `test_tag_management.py` 测试脚本
- 创建了 `c3_verify_day3.py` C3 验证脚本
- 所有功能测试通过 ✅
- 原有 35 个测试全部通过 ✅

## 技术细节

### Tag 模型新增方法

```python
@staticmethod
def get_all_tags_with_count():
    """获取所有标签及其使用次数"""
    return db.session.query(Tag, func.count(post_tags.c.post_id).label('count'))\
        .outerjoin(post_tags)\
        .group_by(Tag.id)\
        .order_by(db.desc('count'))\
        .all()

@staticmethod
def cleanup_unused_tags():
    """删除未使用的标签"""
    unused_tags = db.session.query(Tag)\
        .outerjoin(post_tags)\
        .group_by(Tag.id)\
        .having(func.count(post_tags.c.post_id) == 0)\
        .all()
    
    count = len(unused_tags)
    for tag in unused_tags:
        db.session.delete(tag)
    
    if count > 0:
        db.session.commit()
    
    return count

@property
def post_count(self):
    """获取该标签关联的文章数量"""
    return self.posts.count()
```

### 视图函数

```python
@main.route('/manage-tags')
@login_required
@admin_required
def manage_tags():
    """标签管理页面（仅管理员）"""
    tags_with_count = Tag.get_all_tags_with_count()
    return render_template('manage_tags.html', tags_with_count=tags_with_count)

@main.route('/cleanup-tags', methods=['POST'])
@login_required
@admin_required
def cleanup_tags():
    """清理未使用的标签"""
    count = Tag.cleanup_unused_tags()
    flash(f'Successfully cleaned up {count} unused tag(s).')
    return redirect(url_for('.manage_tags'))

@main.route('/delete-tag/<int:tag_id>', methods=['POST'])
@login_required
@admin_required
def delete_tag(tag_id):
    """删除指定标签"""
    tag = Tag.query.get_or_404(tag_id)
    tag_name = tag.name
    db.session.delete(tag)
    db.session.commit()
    flash(f'Tag "{tag_name}" has been deleted.')
    return redirect(url_for('.manage_tags'))
```

## C3 验证结果

### 功能完整性
- ✅ Tag 模型扩展：get_all_tags_with_count()
- ✅ Tag 模型扩展：cleanup_unused_tags()
- ✅ Tag 模型扩展：post_count 属性
- ✅ 路由：/manage-tags (管理页面)
- ✅ 路由：/cleanup-tags (清理未使用标签)
- ✅ 路由：/delete-tag/<id> (删除指定标签)
- ✅ 模板：manage_tags.html
- ✅ 导航栏：管理员可见的标签管理入口
- ✅ 权限控制：仅管理员可访问
- ✅ 数据一致性验证通过

### 测试结果
```
Week 6 Day 3 - 标签管理功能测试
- 创建测试标签: ✅
- 关联标签到文章: ✅
- get_all_tags_with_count(): ✅
- post_count 属性: ✅
- cleanup_unused_tags(): ✅ (清理了 2 个未使用标签)
- 删除特定标签: ✅

原有测试套件: 35/35 通过 ✅
```

## 用户场景测试

### 管理员操作流程
1. ✅ 登录管理员账号
2. ✅ 点击导航栏"Manage Tags"
3. ✅ 查看所有标签及使用次数
4. ✅ 点击"Clean Up Unused Tags"清理未使用标签
5. ✅ 点击单个标签的"Delete"按钮删除指定标签
6. ✅ 查看统计信息（总标签数、未使用标签数）

### 权限验证
- ✅ 非管理员用户看不到"Manage Tags"菜单
- ✅ 直接访问 /manage-tags 会重定向到登录页

## 文件变更

### 修改的文件
- `app/models.py`: 添加标签管理相关方法
- `app/main/views.py`: 添加标签管理路由和视图
- `app/templates/base.html`: 添加管理员导航链接

### 新增的文件
- `app/templates/manage_tags.html`: 标签管理页面模板
- `test_tag_management.py`: 标签管理功能测试脚本
- `c3_verify_day3.py`: C3 验证脚本

## 下一步计划

### Day 3 剩余任务
- ✅ 添加标签管理功能（删除未使用的标签）
- ⏳ 优化标签输入体验（自动补全）
- ⏳ 添加标签系统的单元测试
- ⏳ 准备 PR 描述文档

### 待完成
1. 标签输入自动补全功能
2. 为标签系统编写单元测试
3. 编写 PR 描述文档

## 协作体验

### 今天的收获
- 学会了使用 SQLAlchemy 的 `outerjoin` 和 `having` 子句
- 掌握了 Flask 权限装饰器的使用
- 理解了管理后台的设计模式
- 学会了编写完整的功能验证脚本

### 技术亮点
- 使用 `outerjoin` 确保未使用的标签也能被查询到
- 使用 `having` 子句过滤聚合结果
- 权限控制使用装饰器模式，代码简洁
- 删除操作有二次确认，防止误操作

### 代码质量
- 所有新功能都有测试覆盖
- C3 验证脚本确保功能完整性
- 原有测试全部通过，无回归问题
