from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(
            username='myusername',
            password='MyPassword'
        )
        self.client.login(
            username='myusername',
            password='MyPassword'
        )

        response = self.client.get(reverse('authors:logout'), follow=True)
        self.assertIn(
            'Invalid logout request',
            response.content.decode('utf-8')
            )

    def test_user_tries_to_logout_another_user(self):
        User.objects.create_user(
            username='myusername',
            password='mypassword'
        )

        self.client.login(username='myusername', password='mypassword')

        response = self.client.post(
            reverse('authors:logout'),
            data={'username': 'another_user'},
            follow=True
        )

        self.assertIn(
            'Invalid logout user',
            response.content.decode('utf-8')
        )

    def test_user_can_logout_successfully(self):
        User.objects.create_user(
            username='myusername',
            password='mypassword'
        )

        self.client.login(username='myusername', password='mypassword')

        response = self.client.post(
            reverse('authors:logout'),
            data={'username': 'myusername'},
            follow=True
        )

        self.assertIn(
            'logged out successfuly',
            response.content.decode('utf-8')
        )
