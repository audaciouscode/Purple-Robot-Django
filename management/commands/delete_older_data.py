# pylint: disable=line-too-long, no-member

import datetime

from django.core.management.base import BaseCommand

from ...models import PurpleRobotReading, PurpleRobotPayload, PurpleRobotEvent
from ...decorators import handle_lock

class Command(BaseCommand):
    @handle_lock
    def handle(self, *args, **options):
        end = datetime.datetime.now() - datetime.timedelta(days=14)

        PurpleRobotPayload.objects.filter(added__lte=end).delete()
        PurpleRobotReading.objects.filter(logged__lte=end).delete()
        PurpleRobotEvent.objects.filter(logged__lte=end).delete()
