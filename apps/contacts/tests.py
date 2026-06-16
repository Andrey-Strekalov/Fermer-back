from unittest.mock import MagicMock, patch

from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.bids.models import Bid
from apps.notifications.models import Notification
from apps.users.models import User

CONTACTS_URL = '/api/v1/contact-requests/'


def auth_headers(user):
    token = RefreshToken.for_user(user)
    return {'HTTP_AUTHORIZATION': f'Bearer {str(token.access_token)}'}


class ContactRequestTests(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user(phone_number='+79001230010', password='x')
        self.sender = User.objects.create_user(phone_number='+79001230011', password='x')
        self.bid = Bid.objects.create(
            author=self.author,
            type='sell',
            title='Кукуруза',
            price='3000.00',
            volume='50.000',
            region='Ростовская область',
        )

    def _post(self, user, bid_id=None, comment='Хочу купить'):
        return self.client.post(
            CONTACTS_URL,
            {'bid_id': bid_id or self.bid.id, 'comment': comment},
            format='json',
            **auth_headers(user),
        )

    @patch('apps.contacts.views.async_to_sync')
    @patch('apps.contacts.views.get_channel_layer')
    def test_create_contact_request_returns_201_and_creates_notification(
        self, mock_layer, mock_async
    ):
        mock_async.return_value = MagicMock()
        before = Notification.objects.count()
        resp = self._post(self.sender)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Notification.objects.count(), before + 1)

    @patch('apps.contacts.views.async_to_sync')
    @patch('apps.contacts.views.get_channel_layer')
    def test_duplicate_contact_request_returns_409(self, mock_layer, mock_async):
        # NOTE: код возвращает 409 Conflict, а не 400 Bad Request
        mock_async.return_value = MagicMock()
        self._post(self.sender)
        resp = self._post(self.sender)
        self.assertEqual(resp.status_code, 409)

    def test_contact_request_on_own_bid_returns_400(self):
        resp = self._post(self.author)
        self.assertEqual(resp.status_code, 400)
