from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User

BIDS_URL = '/api/v1/bids/'

BID_PAYLOAD = {
    'type': 'sell',
    'title': 'Пшеница озимая',
    'price': '5000.00',
    'volume': '100.000',
    'region': 'Краснодарский край',
}


def auth_headers(user):
    token = RefreshToken.for_user(user)
    return {'HTTP_AUTHORIZATION': f'Bearer {str(token.access_token)}'}


class BidCRUDTests(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user(phone_number='+79001230001', password='x')
        self.other = User.objects.create_user(phone_number='+79001230002', password='x')

    def _create_bid(self, user=None):
        return self.client.post(
            BIDS_URL, BID_PAYLOAD, format='json', **auth_headers(user or self.author)
        )

    def test_create_bid_authenticated_returns_201(self):
        resp = self._create_bid()
        self.assertEqual(resp.status_code, 201)

    def test_create_bid_anonymous_returns_401(self):
        resp = self.client.post(BIDS_URL, BID_PAYLOAD, format='json')
        self.assertEqual(resp.status_code, 401)

    def test_list_bids_returns_200_with_expected_keys(self):
        resp = self.client.get(BIDS_URL, **auth_headers(self.author))
        self.assertEqual(resp.status_code, 200)
        for key in ('success', 'items', 'total'):
            self.assertIn(key, resp.data)

    def test_archive_bid_by_author_returns_200(self):
        bid_id = self._create_bid().data['bid']['id']
        resp = self.client.patch(
            f'{BIDS_URL}{bid_id}/archive/', **auth_headers(self.author)
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data['bid']['is_archived'])

    def test_delete_bid_by_other_user_returns_403(self):
        bid_id = self._create_bid().data['bid']['id']
        resp = self.client.delete(
            f'{BIDS_URL}{bid_id}/', **auth_headers(self.other)
        )
        self.assertEqual(resp.status_code, 403)
