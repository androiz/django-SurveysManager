from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

# Create your tests here.

class TokenTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client(HTTP_HOST='testserver')

    def test_create_user(self):
        form = {
            'name': 'Fred',
            'surname': 'Weasly',
            'email': 'fred.weasly@hp.hp',
            'password': 'george'
        }

        response = self.client.post('/sign_up/', form)
        fred = User.objects.get(email="fred.weasly@hp.hp")


        self.assertRedirects(response, "/", status_code=302, target_status_code=200, host=None,
                                       msg_prefix='', fetch_redirect_response=True)

        self.assertEqual(fred.is_active, False)