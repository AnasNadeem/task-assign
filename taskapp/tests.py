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
        data = self.deserialize(self.api_client.post('/api/register/', format='json', data=user_data))
        return self.create_apikey(data['username'], data['token'])

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
        self.assertHttpCreated(self.api_client.post('/api/task/', format='json',authentication=self.get_credentials(self.user_data), data=self.task_data))

    # def test_user_update_task(self):
    #     pass

    # def test_user_can_view_other_task(self):
    #     new_user = {
    #         'username':'test1',
    #         'password':'test'
    #     }
    #     data = self.deserialize(self.api_client.post('/api/task/', format='json',authentication=self.get_credentials(new_user), data=self.task_data))
    #     self.assertHttpUnauthorized(self.api_client.get(f"/api/task/{data['id']}", format='json',authentication=self.get_credentials(self.user_data)))

    # def test_user_can_edit_other_task(self):
    #     pass