# pylint: disable=line-too-long, no-member

import hashlib
import json

import requests

from requests.exceptions import ConnectionError, ReadTimeout

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import PurpleRobotPayload, PurpleRobotReading
from ...decorators import handle_lock

PRINT_PROGRESS = False

class Command(BaseCommand):
    @handle_lock
    def handle(self, *args, **options): # pylint: disable=too-many-locals, too-many-branches, too-many-statements
        try:
            settings.PR_REDIRECT_ENDPOINT_MAP
        except AttributeError:
            print 'PR_REDIRECT_ENDPOINT_MAP not defined in settings.py. Exiting...'

            return

        tag = 'reflected_payload'

        requests.packages.urllib3.disable_warnings()

        for config in settings.PR_REDIRECT_ENDPOINT_MAP: # pylint: disable=too-many-nested-blocks
            payloads = list(PurpleRobotPayload.objects.filter(user_id=config['hash']).exclude(process_tags__contains=tag)[:50])

            while payloads:
                reflected_payloads = []

                if PRINT_PROGRESS:
                    print 'COUNT: ' + str(len(payloads))

                index = 0

                for pr_payload in payloads:
                    index += 1
                    if PRINT_PROGRESS:
                        print ' PAYLOAD: ' + str(index) + ' -- ' + str(pr_payload.pk)

                    payload = {}
                    payload['Payload'] = pr_payload.payload
                    payload['Operation'] = 'SubmitProbes'

                    md5_hash = hashlib.md5() # nosec
                    md5_hash.update(config['new_id'].encode('utf-8'))
                    payload['UserHash'] = md5_hash.hexdigest()

                    md5_hash = hashlib.md5() # nosec
                    md5_hash.update((payload['UserHash'] + payload['Operation'] + payload['Payload']).encode('utf-8'))
                    payload['Checksum'] = md5_hash.hexdigest()

                    data = {'json': json.dumps(payload, indent=2)}

                    files = {}

                    if 'media_url' in pr_payload.payload:
                        readings = json.loads(pr_payload.payload)

                        for reading in readings:
                            if 'media_url' in reading:
                                pr_reading = PurpleRobotReading.objects.filter(guid=reading['GUID']).first()

                                if pr_reading is not None and pr_reading.attachment is not None:
                                    reading_json = json.loads(pr_reading.payload)

                                    filename = pr_reading.attachment.name.split('/')[-1]
                                    files[pr_reading.guid] = (filename, pr_reading.attachment, reading_json['media_content_type'],)
                    try:
                        response = requests.post(config['endpoint'], data=data, timeout=120.0, files=files)

                        response_obj = json.loads(response.text)

                        if response_obj['Status'] == 'success':
                            reflected_payloads.append(pr_payload.pk)
                    except ValueError:
                        # Missing attachment error - continue on...
                        reflected_payloads.append(pr_payload.pk)
                    except ConnectionError:
                        pass
                    except ReadTimeout:
                        pass

                for primary_key in reflected_payloads:
                    pr_payload = PurpleRobotPayload.objects.get(pk=primary_key)

                    tags = pr_payload.process_tags

                    if tags is None or tags.find(tag) == -1:
                        if tags is None or len(tags) == 0: # pylint: disable=len-as-condition
                            tags = tag
                        else:
                            tags += ' ' + tag

                        pr_payload.process_tags = tags

                        pr_payload.save()

                payloads = list(PurpleRobotPayload.objects.filter(user_id=config['hash']).exclude(process_tags__contains=tag)[:50])
