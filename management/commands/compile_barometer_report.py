# pylint: disable=line-too-long, no-member

import datetime
import gzip
import json
import sys
import tempfile

from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone

from purple_robot.settings import REPORT_DEVICES
from purple_robot_app.models import PurpleRobotReading, PurpleRobotReport

PROBE_NAME = 'edu.northwestern.cbits.purple_robot_manager.probes.builtin.PressureProbe'


class Command(BaseCommand):
    def handle(self, *args, **options):
        hashes = REPORT_DEVICES  # PurpleRobotPayload.objects.order_by().values('user_id').distinct()

        start = datetime.datetime.now() - datetime.timedelta(days=21)

        for user_hash in hashes:
            payloads = PurpleRobotReading.objects.filter(user_id=user_hash, probe=PROBE_NAME, logged__gte=start).order_by('logged')

            count = payloads.count()
            if count > 0:
                temp_file = tempfile.TemporaryFile()
                gzf = gzip.GzipFile(mode='wb', fileobj=temp_file)

                gzf.write('User ID\tSensor Timestamp\ttNormalized Timestamp\tCPU Timestamp\tAltitude\tPressure\n')

                index = 0

                last_sensor = sys.maxint
                base_ts = 0

                while index < count:
                    end = index + 100

                    if end > count:
                        end = count

                    for payload in payloads[index:end]:
                        reading_json = json.loads(payload.payload)

                        normal_times = []
                        sensor_times = []
                        cpu_times = []
                        x_readings = []
                        y_readings = []

                        has_sensor = False

                        if 'SENSOR_TIMESTAMP' in reading_json:
                            has_sensor = True

                            for sensor_time in reading_json['SENSOR_TIMESTAMP']:
                                sensor_times.append(sensor_time)

                        for event_time in reading_json['EVENT_TIMESTAMP']:
                            cpu_times.append(event_time)

                            if has_sensor is False:
                                sensor_times.append(-1)
                                normal_times.append(-1)

                        if has_sensor:
                            for i in range(0, len(sensor_times)):
                                sensor_ts = float(sensor_times[i])

                                normalized_ts = sensor_ts / (1000 * 1000 * 1000)

                                if normalized_ts < last_sensor:
                                    cpu_time = cpu_times[i]

                                    base_ts = cpu_time - normalized_ts

                                normal_times.append(base_ts + normalized_ts)

                                last_sensor = normalized_ts

                        for x_reading in reading_json['ALTITUDE']:
                            x_readings.append(x_reading)

                        for y_reading in reading_json['PRESSURE']:
                            y_readings.append(y_reading)

                        for i in range(0, len(cpu_times)):
                            x_reading = x_readings[i]
                            y_reading = y_readings[i]
                            cpu_time = cpu_times[i]
                            sensor_time = sensor_times[i]
                            normal_time = normal_times[i]

                            gzf.write(user_hash + '\t' + str(sensor_time) + '\t' + str(normal_time) + '\t' + str(cpu_time) + '\t' + str(x_reading) + '\t' + str(y_reading) + '\n')

                    index += 100

                gzf.flush()
                gzf.close()

                temp_file.seek(0)

                report = PurpleRobotReport(generated=timezone.now(), mime_type='application/x-gzip', probe=PROBE_NAME, user_id=user_hash)
                report.save()
                report.report_file.save(user_hash + '-barometer.txt.gz', File(temp_file))
                report.save()
