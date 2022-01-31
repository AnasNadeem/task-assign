from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from tastypie.authorization import Authorization
from django.db import IntegrityError
from tastypie.exceptions import BadRequest
from tastypie.models import ApiKey
from django.urls import path
from tastypie.http import HttpUnauthorized

class AuthResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth'
        allowed_methods = ['post']
        authorization = Authorization()
        fields = ['username', 'id']
        excludes = ['password']
        always_return_data = True

    def prepend_urls(self):
        return [
            path('register/', self.wrap_view('register'), name="api_register"),
            path('login/', self.wrap_view('login'), name="api_login"),
            path('logout/', self.wrap_view('logout'), name="api_logout")
        ]

    def register(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body)
        username = data.get('username')
        password = data.get('password')
        if username is None or password is None:
            raise BadRequest('Please enter a value.')

        try:
            user = User.objects.create_user(username, '', password)
            # Getting the API key 
            api_key = ApiKey.objects.get(user=user.id)
            return self.create_response(request, {
                    'success': True,
                    'username':username,
                    'token': api_key.key
            })
        except IntegrityError:
            raise BadRequest('That username already exists')

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body)
        username = data.get('username')
        password = data.get('password')
        if username is None or password is None:
            raise BadRequest('Please enter a value.')

        # Check if the user exists
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            # Getting the API key,create if doesn't exist
            try:
                api_key = ApiKey.objects.get(user=user)
                if not api_key.key:
                    api_key.save()
            except ApiKey.DoesNotExist:
                api_key = ApiKey.objects.create(user=user)

            return self.create_response(request, {
                    'success': True,
                    'username':username,
                    'token': api_key.key
                })
        else:
            raise BadRequest("Incorrect username or password.")
    
    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.authenticated():
            logout(request)
            return self.request.create_response(request, {'success': True})
        else:
            return self.request.create_response(request, {'success': False}, HttpUnauthorized)