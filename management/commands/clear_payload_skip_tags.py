# pylint: disable=line-too-long, no-member

import requests

from django.core.management.base import BaseCommand

from ...models import PurpleRobotPayload
from ...decorators import handle_lock

PRINT_PROGRESS = False

SKIP_TAG = 'extracted_into_database_skip'

class Command(BaseCommand):
    @handle_lock
    def handle(self, *args, **options):
        requests.packages.urllib3.disable_warnings()

        payloads = list(PurpleRobotPayload.objects.filter(process_tags__contains=SKIP_TAG).order_by('-added')[:250])

        count = 0

        while payloads and count < 20:
            count += 1

            for payload in payloads:
                payload.process_tags = payload.process_tags.replace(SKIP_TAG, '')

                while payload.process_tags.find('  ') != -1:
                    payload.process_tags = payload.process_tags.replace('  ', ' ')

                payload.process_tags = payload.process_tags.strip()

                payload.save()

            payloads = list(PurpleRobotPayload.objects.filter(process_tags__contains=SKIP_TAG).order_by('-added')[:250])
