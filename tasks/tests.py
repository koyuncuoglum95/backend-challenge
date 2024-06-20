from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import Task, Label

class APITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.label = Label.objects.create(name='Work', owner=self.user)
        self.task = Task.objects.create(title='Task 1', description='Task description', completed=False, owner=self.user)
        self.task.labels.add(self.label)

    def test_get_tasks(self):
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Task 1')

    def test_get_labels(self):
        response = self.client.get('/api/labels/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Work')

    def test_create_task(self):
        data = {
            'title': 'New Task',
            'description': 'New task description',
            'completed': False,
            'labels': [self.label.id],
            'owner': self.user.id
        }
        response = self.client.post('/api/tasks/', data)
        print(response.content)  # Print the response content for debugging
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.last().title, 'New Task')

    def test_create_label(self):
        data = {
            'name': 'New Label',
            'owner': self.user.id
        }
        response = self.client.post('/api/labels/', data)
        print(response.content)  # Print the response content for debugging
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Label.objects.count(), 2)
        self.assertEqual(Label.objects.last().name, 'New Label')
