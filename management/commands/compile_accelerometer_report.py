import datetime
import gzip
import json
import pytz
import tempfile
import urllib
import urllib2

from django.core.files import File
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from purple_robot_app.models import *
from purple_robot.settings import REPORT_DEVICES

PROBE_NAME = 'edu.northwestern.cbits.purple_robot_manager.probes.builtin.AccelerometerProbe'

class Command(BaseCommand):
    def handle(self, *args, **options):
        hashes = REPORT_DEVICES # PurpleRobotPayload.objects.order_by().values('user_id').distinct()
        
        start = datetime.datetime.now() - datetime.timedelta(days=21)

        for hash in hashes:
            # hash = hash['user_id']

            payloads = PurpleRobotReading.objects.filter(user_id=hash, probe=PROBE_NAME, logged__gte=start).order_by('logged')
            
            count = payloads.count()
            if count > 0:
                temp_file = tempfile.TemporaryFile()

                gzf = gzip.GzipFile(mode='wb', fileobj=temp_file)
                gzf.write('User ID\tSensor Timestamp\tCPU Timestamp\tX\tY\tZ\n')
                
                index = 0
                
                while index < count:
                    end = index + 100
                    
                    if end > count:
                        end = count
                
                    for payload in payloads[index:end]:
                        reading_json = json.loads(payload.payload)
                        
                        ss = []
                        ts = []
                        xs = []
                        ys = []
                        zs = []
                        
                        has_sensor = False
                        
                        if 'SENSOR_TIMESTAMP' in reading_json:
                            has_sensor = True
                            
                            for s in reading_json['SENSOR_TIMESTAMP']:
                                ss.append(s)

                        for t in reading_json['EVENT_TIMESTAMP']:
                            ts.append(t)
                            
                            if has_sensor == False:
                                ss.append(-1)
    
                        for x in reading_json['X']:
                            xs.append(x)
    
                        for y in reading_json['Y']:
                            ys.append(y)
    
                        for z in reading_json['Z']:
                            zs.append(z)
                    
                        for i in range(0, len(ts)):
                            x = xs[i]
                            y = ys[i]
                            z = zs[i]
                            t = ts[i]
                            s = ss[i]
                            
                            gzf.write(hash + '\t' + str(s) + '\t' + str(t) + '\t' + str(x) + '\t' + str(y) + '\t' + str(z) + '\n')
                            
                    index += 100
                    
                gzf.flush()
                gzf.close()
                
                temp_file.seek(0)
                        
                report = PurpleRobotReport(generated=timezone.now(), mime_type='application/x-gzip', probe=PROBE_NAME, user_id=hash)
                report.save()
                report.report_file.save(hash + '-accelerometer.txt.gz', File(temp_file))
                report.save()
                
                print('Wrote ' + hash + '-accelerometer.txt')
