# Week 6 Day 2 协作日志

## 日期
2026-04-XX

## 今天完成的工作

### 1. 标签系统核心功能实现
- 数据模型：Tag 模型 + post_tags 多对多关联表
- 数据库迁移：成功添加标签表和关联表
- 标签存储：文章可以关联 0-N 个标签

### 2. 标签 UI 功能
- 发文章表单：添加标签输入框（逗号分隔）
- 文章列表：显示文章的标签
- 标签筛选：点击标签可以查看该标签下的所有文章
- 编辑文章：支持修改文章的标签

### 3. 热门标签侧边栏
- 首页右侧显示 Popular Tags
- 按使用次数排序，显示 Top 5
- 显示每个标签的使用次数

### 4. 测试验证
- 运行老测试套件：35 个测试全部通过
- C3 验证：标签数据准确性验证通过
  - ORM 查询与数据库查询一致
  - 标签筛选功能正确
  - 热门标签统计正确

## 技术细节

### 数据模型
```python
# 多对多关系
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    posts = db.relationship('Post', secondary=post_tags, 
                           back_populates='tags', lazy='dynamic')
```

### 标签处理逻辑
- 发文章时解析逗号分隔的标签字符串
- 查找或创建标签对象
- 建立文章-标签关联

### 热门标签查询
```python
top_tags = db.session.query(Tag, db.func.count(post_tags.c.post_id))\
    .join(post_tags)\
    .group_by(Tag.id)\
    .order_by(db.desc('count'))\
    .limit(5)\
    .all()
```

## 遇到的问题和解决方案

### 问题 1：端口占用
- 现象：Flask 服务器启动失败，5001 端口被占用
- 解决：使用 lsof 查找并清理占用端口的进程

### 问题 2：测试工具
- 现象：项目没有安装 pytest
- 解决：使用 unittest 运行测试套件

## 业务验证

### 用户场景测试
1. ✅ 发文章时添加标签（python, flask, web开发）
2. ✅ 文章列表显示标签
3. ✅ 点击标签筛选相关文章
4. ✅ 侧边栏显示热门标签 Top 5
5. ✅ 编辑文章时修改标签

### C3 验证结果
- 标签总数：3 个
- 文章-标签关联：3 条
- ORM 查询与数据库查询一致 ✅
- 标签筛选功能正确 ✅

## 下一步计划

### Day 3 任务
- 添加标签管理功能（删除未使用的标签）
- 优化标签输入体验（自动补全）
- 添加标签系统的单元测试
- 准备 PR 描述文档

## 协作体验

### 今天的收获
- 理解了多对多关系的实现方式
- 学会了使用 SQLAlchemy 进行复杂查询
- 掌握了 Flask 表单和视图的修改流程

### 需要改进的地方
- 标签输入体验可以更好（目前是纯文本输入）
- 热门标签可以增加时间范围筛选（近 30 天）
