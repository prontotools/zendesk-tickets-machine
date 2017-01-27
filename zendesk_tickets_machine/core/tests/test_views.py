from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class LoginViewTest(TestCase):
    def test_need_login(self):
        with self.settings(LOGIN_URL=reverse('login')):
            response = self.client.get('/')
            self.assertRedirects(response, '/login/?next=/')

    def test_login_pass(self):
        User.objects.create_superuser('natty', 'natty@test', 'pass')
        response = self.client.post(reverse('login'), {
            'username': 'natty', 'password': 'pass'})
        self.assertEqual(response.status_code, 302)

    def test_login_fail(self):
        response = self.client.post(reverse('login'), {
            'username': 'john', 'password': 'smith'})
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        User.objects.create_superuser('natty', 'natty@test', 'pass')
        self.client.post(reverse('login'), {
            'username': 'natty', 'password': 'pass'})
        self.client.post(reverse('logout'))
        with self.settings(LOGIN_URL=reverse('login')):
            response = self.client.get('/')
            self.assertRedirects(response, '/login/?next=/')
