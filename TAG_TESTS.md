# 标签系统单元测试文档

## 测试概览

为标签系统添加了全面的单元测试和集成测试，覆盖模型层和视图层的所有功能。

## 测试文件

### 1. test_tag_model.py - 模型层测试

测试 Tag 模型的核心功能：

#### 测试用例

1. **test_tag_creation** - 标签创建
   - 验证标签可以正常创建
   - 验证标签有正确的 ID 和名称

2. **test_tag_post_relationship** - 标签-文章关系
   - 验证多对多关系正确建立
   - 验证文章可以关联多个标签
   - 验证标签可以关联多篇文章

3. **test_tag_post_count** - 文章计数
   - 验证 `post_count` 属性返回正确的文章数量

4. **test_get_all_tags_with_count** - 获取所有标签及计数
   - 验证返回所有标签（包括未使用的）
   - 验证标签按使用次数降序排列
   - 验证未使用标签的计数为 0

5. **test_cleanup_unused_tags** - 清理未使用标签
   - 验证能正确识别未使用的标签
   - 验证能删除所有未使用的标签
   - 验证已使用的标签不会被删除

6. **test_tag_unique_constraint** - 唯一性约束
   - 验证标签名称的唯一性约束
   - 验证重复标签名会抛出异常

7. **test_tag_repr** - 字符串表示
   - 验证标签的 `__repr__` 方法

### 2. test_tag_client.py - 视图层集成测试

测试标签相关的 HTTP 端点和用户交互：

#### 测试用例

1. **test_api_tags_endpoint** - API 端点
   - 验证 `/api/tags` 返回 JSON 格式的标签列表
   - 验证返回的标签名称正确

2. **test_create_post_with_tags** - 创建带标签的文章
   - 验证用户可以在发文章时添加标签
   - 验证标签会自动创建（如果不存在）
   - 验证文章正确关联标签

3. **test_posts_by_tag** - 按标签筛选文章
   - 验证 `/tag/<tag_name>` 路由正常工作
   - 验证页面显示正确的文章

4. **test_manage_tags_requires_admin** - 管理员权限
   - 验证未登录用户无法访问标签管理
   - 验证普通用户无法访问标签管理
   - 验证返回正确的 HTTP 状态码

5. **test_cleanup_tags_endpoint** - 清理标签端点
   - 验证管理员可以清理未使用的标签
   - 验证清理操作正确执行
   - 验证已使用的标签不受影响

6. **test_delete_tag_endpoint** - 删除标签端点
   - 验证管理员可以删除指定标签
   - 验证标签从数据库中移除

7. **test_edit_post_tags** - 编辑文章标签
   - 验证用户可以修改文章的标签
   - 验证旧标签被正确移除
   - 验证新标签被正确添加

## 测试统计

- **总测试数**: 49 个
- **新增测试**: 14 个（7 个模型测试 + 7 个集成测试）
- **测试通过率**: 100%
- **跳过测试**: 1 个（Selenium 测试，需要浏览器驱动）

## 测试覆盖

### 模型层覆盖
- ✅ Tag 模型创建
- ✅ 多对多关系（Tag ↔ Post）
- ✅ 标签统计方法
- ✅ 标签清理功能
- ✅ 数据库约束

### 视图层覆盖
- ✅ API 端点（/api/tags）
- ✅ 标签管理页面（/manage-tags）
- ✅ 清理标签（/cleanup-tags）
- ✅ 删除标签（/delete-tag/<id>）
- ✅ 按标签筛选（/tag/<name>）
- ✅ 权限控制（@admin_required）

### 用户场景覆盖
- ✅ 发文章时添加标签
- ✅ 编辑文章时修改标签
- ✅ 管理员管理标签
- ✅ 普通用户查看标签

## 运行测试

```bash
# 运行所有测试
python -m unittest discover tests

# 运行标签相关测试
python -m unittest tests.test_tag_model
python -m unittest tests.test_tag_client

# 运行单个测试
python -m unittest tests.test_tag_model.TagModelTestCase.test_tag_creation
```

## 测试结果示例

```
Ran 49 tests in 5.252s

OK (skipped=1)
```

## 代码质量

- 所有测试都有清晰的文档字符串
- 使用 setUp 和 tearDown 确保测试隔离
- 测试覆盖正常流程和边界情况
- 测试数据在每个测试后清理
- 遵循 AAA 模式（Arrange-Act-Assert）
