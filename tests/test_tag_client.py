import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Post, Tag, Role


class TagClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_api_tags_endpoint(self):
        # Create some tags
        tag1 = Tag(name='python')
        tag2 = Tag(name='flask')
        db.session.add_all([tag1, tag2])
        db.session.commit()

        # Test API endpoint
        response = self.client.get('/api/tags')
        self.assertEqual(response.status_code, 200)
        import json
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertIn('python', data)
        self.assertIn('flask', data)

    def test_create_post_with_tags(self):
        # Register and login
        response = self.client.post('/auth/register', data={
            'email': 'john@example.com',
            'username': 'john',
            'password': 'cat',
            'password2': 'cat'
        })
        self.assertEqual(response.status_code, 302)

        # Confirm account
        user = User.query.filter_by(email='john@example.com').first()
        token = user.generate_confirmation_token()
        user.confirm(token)
        db.session.add(user)
        db.session.commit()

        # Login
        response = self.client.post('/auth/login', data={
            'email': 'john@example.com',
            'password': 'cat'
        }, follow_redirects=True)

        # Create post with tags
        response = self.client.post('/', data={
            'body': 'Test post with tags',
            'tags': 'python, flask, web'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Verify tags were created
        self.assertEqual(Tag.query.count(), 3)
        python_tag = Tag.query.filter_by(name='python').first()
        self.assertIsNotNone(python_tag)

        # Verify post has tags
        post = Post.query.first()
        self.assertEqual(post.tags.count(), 3)

    def test_posts_by_tag(self):
        # Create user and post with tag
        user = User(email='test@example.com', username='test', password='cat')
        tag = Tag(name='python')
        post = Post(body='Python post', author=user, tags=[tag])
        db.session.add_all([user, tag, post])
        db.session.commit()

        # Test tag filter page
        response = self.client.get('/tag/python')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Python post', response.data)

    def test_manage_tags_requires_admin(self):
        # Try to access without login
        response = self.client.get('/manage-tags')
        self.assertEqual(response.status_code, 302)  # Redirect to login

        # Register and login as regular user
        response = self.client.post('/auth/register', data={
            'email': 'john@example.com',
            'username': 'john',
            'password': 'cat',
            'password2': 'cat'
        })

        user = User.query.filter_by(email='john@example.com').first()
        token = user.generate_confirmation_token()
        user.confirm(token)
        db.session.add(user)
        db.session.commit()

        self.client.post('/auth/login', data={
            'email': 'john@example.com',
            'password': 'cat'
        })

        # Regular user should not access
        response = self.client.get('/manage-tags', follow_redirects=True)
        self.assertEqual(response.status_code, 403)

    def test_cleanup_tags_endpoint(self):
        # Create admin user
        admin_role = Role.query.filter_by(name='Administrator').first()
        admin = User(email='admin@example.com', username='admin',
                    password='cat', role=admin_role, confirmed=True)

        # Create tags
        tag1 = Tag(name='used')
        tag2 = Tag(name='unused')
        post = Post(body='Test', author=admin, tags=[tag1])
        db.session.add_all([admin, tag1, tag2, post])
        db.session.commit()

        # Login as admin
        self.client.post('/auth/login', data={
            'email': 'admin@example.com',
            'password': 'cat'
        })

        # Cleanup unused tags
        response = self.client.post('/cleanup-tags', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Verify unused tag was deleted
        self.assertEqual(Tag.query.count(), 1)
        self.assertEqual(Tag.query.first().name, 'used')

    def test_delete_tag_endpoint(self):
        # Create admin user
        admin_role = Role.query.filter_by(name='Administrator').first()
        admin = User(email='admin@example.com', username='admin',
                    password='cat', role=admin_role, confirmed=True)

        # Create tag
        tag = Tag(name='to-delete')
        db.session.add_all([admin, tag])
        db.session.commit()
        tag_id = tag.id

        # Login as admin
        self.client.post('/auth/login', data={
            'email': 'admin@example.com',
            'password': 'cat'
        })

        # Delete tag
        response = self.client.post(f'/delete-tag/{tag_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Verify tag was deleted
        self.assertIsNone(Tag.query.get(tag_id))

    def test_edit_post_tags(self):
        # Create user and post
        user = User(email='test@example.com', username='test',
                   password='cat', confirmed=True)
        tag1 = Tag(name='old-tag')
        post = Post(body='Test post', author=user, tags=[tag1])
        db.session.add_all([user, tag1, post])
        db.session.commit()
        post_id = post.id

        # Login
        self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'cat'
        })

        # Edit post tags
        response = self.client.post(f'/edit/{post_id}', data={
            'body': 'Updated post',
            'tags': 'new-tag, another-tag'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Verify tags were updated
        post = Post.query.get(post_id)
        self.assertEqual(post.tags.count(), 2)
        tag_names = [tag.name for tag in post.tags]
        self.assertIn('new-tag', tag_names)
        self.assertIn('another-tag', tag_names)
        self.assertNotIn('old-tag', tag_names)
