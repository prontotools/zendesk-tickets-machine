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
        response = self.client.post(
            reverse('login'),
            {'username': 'natty', 'password': 'pass'}
        )
        self.assertEqual(response.status_code, 302)

    def test_login_fail(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'john', 'password': 'smith'}
        )
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        User.objects.create_superuser('natty', 'natty@test', 'pass')
        self.client.post(
            reverse('login'),
            {'username': 'natty', 'password': 'pass'}
        )
        self.client.post(reverse('logout'))
        with self.settings(LOGIN_URL=reverse('login')):
            response = self.client.get('/')
            self.assertRedirects(response, '/login/?next=/')

    def test_login_page_should_have_title(self):
        response = self.client.get(reverse('login'))

        expected = '<title>Login | Pronto Zendesk Tickets Machine</title>'
        self.assertContains(response, expected, count=1, status_code=200)

    def test_login_page_should_have_login_form(self):
        response = self.client.get(reverse('login'))

        expected = '<form class="form-signin" method="post" action="/login/">'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<input type=\'hidden\' name=\'csrfmiddlewaretoken\''
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="form-signin-heading">' \
            '<img src="/static/img/pronto-logo-header.png" width="150px">' \
            '</div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<input type="text" class="form-control" ' \
            'placeholder="Username" required="" autofocus="" ' \
            'maxlength="254" id="id_username" name="username">'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<input type="password" class="form-control" ' \
            'placeholder="Password" required="" id="id_password" ' \
            'name="password">'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<button class="btn btn-lg btn-primary btn-block" ' \
            'type="submit">Log In</button>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<input type="hidden" name="next" ' \
            'value="/accounts/profile/" />'
        self.assertContains(response, expected, count=1, status_code=200)

    def test_login_fail_should_have_login_error_message(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'john', 'password': 'smith'}
        )
        expected = '<div class="text-center alert alert-danger">' \
            'Incorrect username or password.</div>'
        self.assertContains(response, expected, count=1, status_code=200)
