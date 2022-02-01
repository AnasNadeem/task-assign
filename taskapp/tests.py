import imp
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin
from taskapp.models import Task
from django.contrib.auth.models import User
from tastypie.models import ApiKey

# Create your tests here.
class TaskResourceTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super(TaskResourceTest, self).setUp()

        self.user_data = {
            'username':'test',
            'password':'test'
        }

        self.task_data = {
            'title': 'First Post'
        }

    def get_credentials(self, user_data):
        login_data = self.deserialize(self.api_client.post('/api/login/', format='json', data=user_data))
        return self.create_apikey(login_data['username'], login_data['token'])

    def test_register(self):
        self.assertHttpOK(self.api_client.post('/api/register/', format='json', data=self.user_data))

    def test_login_correct_credentials(self):
        self.test_register()
        self.assertHttpOK(self.api_client.post('/api/login/', format='json', data=self.user_data))

    def test_login_incorrect_credentials(self):
        login_data = {
            'username':'test1',
            'password':'test'
        }
        self.assertHttpBadRequest(self.api_client.post('/api/login/', format='json', data=login_data))

    def test_unauthorized_task(self):
        self.assertHttpUnauthorized(self.api_client.post('/api/task/', format='json', data=self.task_data))

    def test_user_create_task(self):
        self.api_client.post('/api/register/', format='json', data=self.user_data)
        self.assertHttpCreated(self.api_client.post('/api/task/', format='json',authentication=self.get_credentials(self.user_data), data=self.task_data))

    def test_user_update_task(self):
        self.test_user_create_task()
        created_task = self.deserialize(self.api_client.get('/api/task/', format='json',authentication=self.get_credentials(self.user_data)))
        update_task_data = {
            'title':'Last'
        }
        self.assertHttpOK(self.api_client.put(f"/api/task/{created_task['objects'][0]['id']}/", format='json',
            authentication=self.get_credentials(self.user_data), data=update_task_data))
        updated_task = self.deserialize(self.api_client.get(f"/api/task/", format='json',authentication=self.get_credentials(self.user_data)))
        self.assertEqual(update_task_data['title'], updated_task['objects'][0]['title'])

    def test_unauth_user_view_task(self):
        new_user = {
            'username':'test1',
            'password':'test'
        }
        self.api_client.post('/api/register/', format='json', data=new_user)
        des_data = self.deserialize(self.api_client.post('/api/task/', format='json',authentication=self.get_credentials(new_user), data=self.task_data))
        self.api_client.post('/api/register/', format='json', data=self.user_data)
        self.assertHttpUnauthorized(self.api_client.get(f"/api/task/{des_data['id']}/", format='json',authentication=self.get_credentials(self.user_data)))

    def test_unauth_user_edit_task(self):
        self.test_user_create_task()
        created_task = self.deserialize(self.api_client.get('/api/task/', format='json',authentication=self.get_credentials(self.user_data)))
        update_task_data = {
            'title':'Last'
        }
        new_user = {
            'username':'test1',
            'password':'test'
        }
        self.api_client.post('/api/register/', format='json', data=new_user)
        self.assertHttpUnauthorized(self.api_client.put(f"/api/task/{created_task['objects'][0]['id']}/", format='json',
            authentication=self.get_credentials(new_user), data=update_task_data))