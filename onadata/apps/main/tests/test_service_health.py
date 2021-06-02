import json
from django.http import HttpRequest
from django.core.cache.backends.base import InvalidCacheBackendError
from mock import patch

from onadata.apps.main.tests.test_base import TestBase
from onadata.apps.main.views import service_health


class TestServiceHealthView(TestBase):
    def test_service_health(self):
        """
        Test that the `service_health` view function
        works as expected:
            1. Returns a 200 when secondary services are healthy
            2. Returns a 500 when a secondary service is not available
        """
        req = HttpRequest()
        resp = service_health(req)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            json.loads(resp.content.decode('utf-8')),
            {
                'default-Database': 'OK',
                'Cache-Service': 'OK'
            })

        with patch('onadata.apps.main.views.cache') as cache_mock:
            cache_mock.set.side_effect = InvalidCacheBackendError(
                'Invalid cache configuration')
            resp = service_health(req)

            self.assertEqual(resp.status_code, 500)
            self.assertEqual(
                json.loads(resp.content.decode('utf-8')),
                {
                    'default-Database': 'OK',
                    'Cache-Service': (
                        'Degraded state; '
                        'Invalid cache configuration')
                })
