# pylint: disable=line-too-long, no-member, invalid-name

from collections import namedtuple

from django.core.management.base import BaseCommand
from django.test.client import RequestFactory

from ...models import PurpleRobotDevice
from ...views import pr_device
from ...decorators import handle_lock

class Command(BaseCommand):
    @handle_lock
    def handle(self, *args, **options):
        FakeRequest = namedtuple('FakeRequest', ['is_active', 'is_staff'])

        factory = RequestFactory()

        request = factory.get('/pr/devices/foobar')
        request.user = FakeRequest(is_active=True, is_staff=True)

        for device in PurpleRobotDevice.objects.all():
            pr_device(request, device.device_id)
