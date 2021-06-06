from rest_framework.test import APIClient
from testing.testcases import TestCase


LOGIN_URL = '/api/accounts/login/'
LOGOUT_URL = '/api/accounts/logout/'
SIGNUP_URL = '/api/accounts/signup/'
LOGIN_STATUS_URL = '/api/accounts/login_status/'


class AccountApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = self.create_user(
            username='admin',
            email='admin@twitter.com',
            password='correct password',
        )

#    def create_user(self, username, email, password):
#       return User.objects.create_user(username, email, password)

    def test_login(self):

        # GET instead of POST
        response = self.client.get(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })
        # failed login, http status code = 405 METHOD_NOT_ALLOWED
        self.assertEqual(response.status_code, 405)

        # POST with wrong password
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'wrong password',
        })
        self.assertEqual(response.status_code, 400)

        # login status should indicate failed login
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)
        # login using correct password
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['user'], None)
        self.assertEqual(response.data['user']['email'], 'admin@twitter.com')
        # login status check
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

    def test_logout(self):
        # login
        self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })
        # login status check
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

        # GET request check
        response = self.client.get(LOGOUT_URL)
        self.assertEqual(response.status_code, 405)

        # POST request check
        response = self.client.post(LOGOUT_URL)
        self.assertEqual(response.status_code, 200)
        # logout status check
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

    def test_signup(self):
        data = {
            'username': 'someone',
            'email': 'someone@twitter.com',
            'password': 'any password',
        }
        # GET request check
        response = self.client.get(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 405)

        # wrong email
        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'not a correct email',
            'password': 'any password'
        })
        # print(response.data)
        self.assertEqual(response.status_code, 400)

        # password too short
        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'someone@twitter.com',
            'password': '123',
        })
        # print(response.data)
        self.assertEqual(response.status_code, 400)

        # username too long
        response = self.client.post(SIGNUP_URL, {
            'username': 'username is tooooooooooooooooo loooooooong',
            'email': 'someone@twitter.com',
            'password': 'any password',
        })
        # print(response.data)
        self.assertEqual(response.status_code, 400)

        # successfully signing up
        response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['username'], 'someone')
        # login status check
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)
