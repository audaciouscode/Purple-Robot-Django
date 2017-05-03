# pylint: disable=line-too-long, no-member

import datetime

from django.core.management.base import BaseCommand

from ...models import PurpleRobotDevice, PurpleRobotPayload, PurpleRobotReading
from ...management.commands.pr_check_status import log_alert, cancel_alert

START_DAYS = 7


class Command(BaseCommand):
    def handle(self, *args, **options):
        start = datetime.datetime.now() - datetime.timedelta(days=START_DAYS)

        for device in PurpleRobotDevice.objects.filter(mute_alerts=False):
            payload = PurpleRobotPayload.objects.filter(user_id=device.hash_key, added__gte=start).order_by('-added').first()
            reading = PurpleRobotReading.objects.filter(user_id=device.hash_key, logged__gte=start).order_by('-logged').first()

            if payload is not None and reading is not None:
                diff = payload.added - reading.logged

                seconds = diff.total_seconds()

                if seconds < (10 * 60):
                    cancel_alert(tags='device_payload_reading_gap', user_id=device.hash_key)
                elif seconds < (30 * 60):
                    log_alert(message='{0:.2f}'.format(seconds / 60) + ' minute gap between payload and reading.', severity=1, tags='device_payload_reading_gap', user_id=device.hash_key)
                else:
                    log_alert(message='{0:.2f}'.format(seconds / 60) + ' minute gap between payload and reading.', severity=2, tags='device_payload_reading_gap', user_id=device.hash_key)
            elif payload is None:
                log_alert(message='Unable to determine reading-payload gap. No payloads uploaded in the last week.', severity=2, tags='device_payload_reading_gap', user_id=device.hash_key)
            elif reading is None:
                log_alert(message='Unable to determine reading-payload gap. No readings uploaded in the last week.', severity=2, tags='device_payload_reading_gap', user_id=device.hash_key)
