import unittest
from app import create_app, db
from app.models import User, Post, Tag, Role


class TagModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_tag_creation(self):
        tag = Tag(name='python')
        db.session.add(tag)
        db.session.commit()
        self.assertIsNotNone(tag.id)
        self.assertEqual(tag.name, 'python')

    def test_tag_post_relationship(self):
        user = User(email='test@example.com', username='test', password='cat')
        tag1 = Tag(name='flask')
        tag2 = Tag(name='python')
        post = Post(body='Test post', author=user, tags=[tag1, tag2])
        db.session.add_all([user, tag1, tag2, post])
        db.session.commit()

        self.assertEqual(post.tags.count(), 2)
        self.assertIn(tag1, post.tags.all())
        self.assertIn(tag2, post.tags.all())
        self.assertEqual(tag1.posts.count(), 1)
        self.assertIn(post, tag1.posts.all())

    def test_tag_post_count(self):
        user = User(email='test@example.com', username='test', password='cat')
        tag = Tag(name='flask')
        post1 = Post(body='Post 1', author=user, tags=[tag])
        post2 = Post(body='Post 2', author=user, tags=[tag])
        db.session.add_all([user, tag, post1, post2])
        db.session.commit()

        self.assertEqual(tag.post_count, 2)

    def test_get_all_tags_with_count(self):
        user = User(email='test@example.com', username='test', password='cat')
        tag1 = Tag(name='flask')
        tag2 = Tag(name='python')
        tag3 = Tag(name='unused')
        post = Post(body='Test post', author=user, tags=[tag1, tag2])
        db.session.add_all([user, tag1, tag2, tag3, post])
        db.session.commit()

        tags_with_count = Tag.get_all_tags_with_count()
        self.assertEqual(len(tags_with_count), 3)

        # Check that tags are ordered by count (descending)
        counts = [count for tag, count in tags_with_count]
        self.assertEqual(counts, sorted(counts, reverse=True))

        # Verify unused tag has count 0
        unused_tag_count = next((count for tag, count in tags_with_count if tag.name == 'unused'), None)
        self.assertEqual(unused_tag_count, 0)

    def test_cleanup_unused_tags(self):
        user = User(email='test@example.com', username='test', password='cat')
        tag1 = Tag(name='used')
        tag2 = Tag(name='unused1')
        tag3 = Tag(name='unused2')
        post = Post(body='Test post', author=user, tags=[tag1])
        db.session.add_all([user, tag1, tag2, tag3, post])
        db.session.commit()

        # Should have 3 tags initially
        self.assertEqual(Tag.query.count(), 3)

        # Clean up unused tags
        count = Tag.cleanup_unused_tags()
        self.assertEqual(count, 2)

        # Should have 1 tag remaining
        self.assertEqual(Tag.query.count(), 1)
        remaining_tag = Tag.query.first()
        self.assertEqual(remaining_tag.name, 'used')

    def test_tag_unique_constraint(self):
        tag1 = Tag(name='python')
        tag2 = Tag(name='python')
        db.session.add(tag1)
        db.session.commit()

        db.session.add(tag2)
        with self.assertRaises(Exception):
            db.session.commit()
        db.session.rollback()

    def test_tag_repr(self):
        tag = Tag(name='flask')
        self.assertEqual(repr(tag), "<Tag 'flask'>")
