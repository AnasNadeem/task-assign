from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from tastypie.authorization import Authorization
from django.db import IntegrityError
from tastypie.exceptions import BadRequest
from tastypie.models import ApiKey
from django.urls import path

class RegisterResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'register'
        allowed_methods = ['post']
        authorization = Authorization()
        fields = ['username', 'id']
        excludes = ['password']
        always_return_data = True

    def obj_create(self, bundle, request=None, **kwargs):
        username = bundle.data.get('username')
        password = bundle.data.get('password')
        if password is None:
            raise BadRequest('Enter Password')
        try:
            bundle.obj = User.objects.create_user(username, '', password)
        except IntegrityError:
            raise BadRequest('That username already exists')
        return bundle

class LoginResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'login'
        allowed_methods = ['post']
        authorization = Authorization()
        fields = ['username', 'id']
        always_return_data = True

    def prepend_urls(self):
        return [
            path('login/', self.wrap_view('login'), name="api_login"),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        # print(dir(request))
        # print(request.body)
        data = self.deserialize(request, request.body)
        username = data.get('username')
        password = data.get('password')
        print(username, password)
        if username is None or password is None:
            raise BadRequest('Please enter a value.')

        # Check if the user exists
        user = authenticate(username=username, password=password)
        if user:
            # Getting the API key 
            api_key = ApiKey.objects.get(user=user.id)
            return self.create_response(request, {
                    'success': True,
                    'username':username,
                    'token': api_key.key
                })
        else:
            raise BadRequest("Incorrect username or password.")
