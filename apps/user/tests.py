from django.test import TestCase
from .models import User


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create('user1', 'password1')
        User.objects.create('user2', 'password2')
        User.objects.create('user3', 'password3')
        User.objects.create('user4', 'password4')
        User.objects.create('user5', 'password5')
