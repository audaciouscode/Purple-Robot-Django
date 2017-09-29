# pylint: disable=line-too-long, no-member

from django.core.management.base import BaseCommand

from ...models import PurpleRobotReading, PurpleRobotDevice
from ...decorators import handle_lock

class Command(BaseCommand):
    @handle_lock
    def handle(self, *args, **options):
        for device in PurpleRobotDevice.objects.all().order_by('device_id'):
            guids = PurpleRobotReading.objects.filter(user_id=device.hash_key).order_by('guid').values_list('guid', flat=True).distinct()

            for guid in guids:
                if guid is not None:
                    count = PurpleRobotReading.objects.filter(guid=guid, user_id=device.hash_key).count()

                    if count > 1:
                        for match in PurpleRobotReading.objects.filter(guid=guid)[1:]:
                            match.delete()
