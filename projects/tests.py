from django.test import TestCase
from django.urls import reverse

from projects.models import Project
from users.models import User


class ProjectTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='owner1@test1.com',
            name='Owner1',
            surname='User1',
            password='123445',
        )
        self.other = User.objects.create_user(
            email='other1@test1.com',
            name='Other1',
            surname='User1',
            password='12314325',
        )
        self.project = Project.objects.create(
            name='Test Project 1', owner=self.user, status='open'
        )
        self.project.participants.add(self.user)

    def test_project_list(self):
        resp = self.client.get(reverse('projects:list'))
        self.assertEqual(resp.status_code, 200)

    def test_create_project(self):
        self.client.login(username='owner1@test1.com', password='123445')
        resp = self.client.post(
            reverse('projects:create'),
            {
                'name': 'New Project 1',
                'description': 'description',
                'github_url': '',
                'status': 'open',
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Project.objects.filter(name='New Project 1').exists())

    def test_toggle_favorite(self):
        self.client.login(username='other1@test1.com', password='12314325')
        resp = self.client.post(
            reverse('projects:toggle_favorite', args=[self.project.pk])
        )
        self.assertTrue(resp.json()['favorited'])
        resp2 = self.client.post(
            reverse('projects:toggle_favorite', args=[self.project.pk])
        )
        self.assertFalse(resp2.json()['favorited'])

    def test_toggle_participate(self):
        self.client.login(username='other1@test1.com', password='12314325')
        resp = self.client.post(
            reverse('projects:toggle_participate', args=[self.project.pk])
        )
        self.assertTrue(resp.json()['participant'])

    def test_complete_project(self):
        self.client.login(username='owner1@test1.com', password='123445')
        resp = self.client.post(
            reverse('projects:complete', args=[self.project.pk])
        )
        self.assertEqual(resp.json()['project_status'], 'closed')

    def test_favorites_list(self):
        self.client.login(username='other1@test1.com', password='12314325')
        self.other.favorites.add(self.project)
        resp = self.client.get(reverse('projects:favorites'))
        self.assertEqual(resp.status_code, 200)
