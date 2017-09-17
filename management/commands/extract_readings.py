# pylint: disable=line-too-long, no-member

from django.core.management.base import BaseCommand
from django.utils import timezone

from ...decorators import handle_lock
from ...models import PurpleRobotReading, PurpleRobotPayload
from ...performance import append_performance_sample


class Command(BaseCommand):
    @handle_lock
    def handle(self, *args, **options):
        tag = 'extracted_readings'

        start = timezone.now()
        payloads = list(PurpleRobotPayload.objects.exclude(process_tags__contains=tag).exclude(process_tags__contains='ingest_error')[:500])
        end = timezone.now()

        query_time = (end - start).total_seconds()

        while payloads:
            start = timezone.now()

            for payload in payloads:
                payload.ingest_readings()

            end = timezone.now()

            perf_values = {}
            perf_values['num_extracted'] = len(payloads)
            perf_values['query_time'] = query_time
            perf_values['extraction_time'] = (end - start).total_seconds()

            append_performance_sample('system', 'reading_ingestion_performance', end, perf_values)

            start = timezone.now()
            payloads = list(PurpleRobotPayload.objects.exclude(process_tags__contains=tag).exclude(process_tags__contains='ingest_error')[:500])
            end = timezone.now()
            query_time = (end - start).total_seconds()

        readings = PurpleRobotReading.objects.filter(guid=None)[:250]

        for reading in readings:
            reading.update_guid()

            readings = PurpleRobotReading.objects.filter(guid=None)[:250]
