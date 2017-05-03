# pylint: disable=unused-argument,line-too-long

import json

def format_reading(probe_name, json_payload):
    item = json.loads(json_payload)
    app = item['CURRENT_APP_NAME']
    category = item['CURRENT_CATEGORY']

    return app + ' (' + category + ')'


def visualize(probe_name, readings):
    return ''

#
#    report = []
#
#    for reading in readings:
#        payload = json.loads(reading.payload)
#
#        timestamp = payload['TIMESTAMP']
#        device_active = payload['DEVICE_ACTIVE']
#
#        if device_active == True:
#            device_active = 1
#        elif device_active == False:
#            device_active = 0
#
#        rep_dict = {}
#        rep_dict["y"] = device_active
#        rep_dict["x"] = timestamp
#        report.append(rep_dict)
#
#    return render_to_string('visualization_device.html', {
#        'probe_name': probe_name,
#        'readings': readings,
#        'device_report': json.dumps(report)
#    })
