from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase

from apps.users.models import PhoneOTP

PHONE = '+79001112233'
REQUEST_CODE_URL = '/api/v1/auth/request-code/'
CONFIRM_CODE_URL = '/api/v1/auth/confirm-code/'
ME_URL = '/api/v1/auth/me/'
REFRESH_URL = '/api/v1/auth/refresh-token/'


class OTPFlowTests(APITestCase):
    def _request_code(self, phone=PHONE):
        return self.client.post(REQUEST_CODE_URL, {'phone': phone}, format='json')

    def _confirm_code(self, code, phone=PHONE):
        return self.client.post(CONFIRM_CODE_URL, {'phone': phone, 'code': code}, format='json')

    def test_request_code_returns_200_and_code(self):
        resp = self._request_code()
        self.assertEqual(resp.status_code, 200)
        self.assertIn('code', resp.data)

    def test_confirm_code_valid_returns_tokens(self):
        code = self._request_code().data['code']
        resp = self._confirm_code(code)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('access_token', resp.data)
        self.assertIn('refresh_token', resp.data)

    def test_confirm_code_invalid_returns_400(self):
        valid_code = self._request_code().data['code']
        # Flip the last digit to guarantee a wrong code without collision risk
        wrong_last = str((int(valid_code[-1]) + 1) % 10)
        wrong_code = valid_code[:-1] + wrong_last
        resp = self._confirm_code(wrong_code)
        self.assertEqual(resp.status_code, 400)

    def test_confirm_code_expired_returns_400(self):
        code = self._request_code().data['code']
        # 400s > OTP_TTL_SECONDS (300s); use .update() to bypass auto_now_add
        PhoneOTP.objects.filter(
            phone_number=PHONE, code=code, is_used=False
        ).update(created_at=timezone.now() - timedelta(seconds=400))
        resp = self._confirm_code(code)
        self.assertEqual(resp.status_code, 400)


class JWTTests(APITestCase):
    PHONE = '+79009998877'

    def setUp(self):
        code = self.client.post(
            REQUEST_CODE_URL, {'phone': self.PHONE}, format='json'
        ).data['code']
        tokens = self.client.post(
            CONFIRM_CODE_URL, {'phone': self.PHONE, 'code': code}, format='json'
        ).data
        self.access_token = tokens['access_token']
        self.refresh_token = tokens['refresh_token']

    def test_me_without_token_returns_401(self):
        resp = self.client.get(ME_URL)
        self.assertEqual(resp.status_code, 401)

    def test_me_with_valid_token_returns_200_with_phone(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        resp = self.client.get(ME_URL)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['user']['phone'], self.PHONE)

    def test_refresh_token_returns_new_access_token(self):
        resp = self.client.post(
            REFRESH_URL, {'refresh_token': self.refresh_token}, format='json'
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn('access_token', resp.data)
