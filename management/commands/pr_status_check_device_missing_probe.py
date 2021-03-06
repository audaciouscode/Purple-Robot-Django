# pylint: disable=line-too-long, no-member

import datetime

from sexpdata import Symbol, Quoted, car, cdr, loads

from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import PurpleRobotDevice, PurpleRobotConfiguration
from ...management.commands.pr_check_status import log_alert, cancel_alert
from ...device_info import can_sense
from ...decorators import handle_lock

TAG = 'expected_probe_missing'
START_DAYS = 7


def enabled_probes(contents): # pylint: disable=too-many-branches
    probes = []

    if isinstance(contents, Symbol):
        pass
    elif isinstance(contents, basestring):
        pass
    elif isinstance(contents, (int, float)):
        pass
    elif isinstance(contents, Quoted):
        return enabled_probes(contents.value())
    elif car(contents) == Symbol('pr-update-probe'):
        probe_name = None
        probe_enabled = False

        for item in cdr(contents):
            if isinstance(item, Quoted):
                item = item.value()

            for child in item:
                if car(child) == 'name':
                    probe_name = cdr(child)
                elif car(child) == 'enabled':
                    probe_enabled = cdr(child)

        if probe_name is not None and probe_enabled and (probe_name in probes) is False:
            probes.append(probe_name)
    else:
        for item in contents:
            found_probes = enabled_probes(item)

            for found in found_probes:
                if (found in probes) is False:
                    probes.append(found)

    if 'Label' in probes:
        probes.remove('Label')

    if 'NfcProbe' in probes:
        probes.remove('NfcProbe')

    return probes


class Command(BaseCommand):
    @handle_lock
    def handle(self, *args, **options): # pylint: disable=too-many-locals, too-many-branches
        start = timezone.now() - datetime.timedelta(days=START_DAYS)

        for device in PurpleRobotDevice.objects.filter(mute_alerts=False).order_by('device_id'):
            model = device.last_model()
            mfgr = device.last_manufacturer()

            config = None

            default = PurpleRobotConfiguration.objects.filter(slug='default').first()

            if device.configuration is not None:
                config = device.configuration
            elif device.device_group is not None and device.device_group.configuration is not None:
                config = device.device_group.configuration
            elif config is None:
                config = default

            if config is None:
                log_alert(message='No configuration associated with ' + device.device_id + '.', severity=2, tags=TAG, user_id=device.hash_key)
            else:
                config_probes = enabled_probes(loads(config.contents, true='#t', false='#f'))

                missing_probes = []

                for probe in config_probes:
                    if can_sense(mfgr, model, probe):
                        found = device.most_recent_reading(probe)

                        if found is None or found.logged < start:
                            missing_probes.append(probe.split('.')[-1])

                platform = device.last_platform()

                if platform is not None and platform.startswith('Android 5'):
                    if 'ApplicationLaunchProbe' in missing_probes:
                        missing_probes.remove('ApplicationLaunchProbe')

                    if 'RunningSoftwareProbe' in missing_probes:
                        missing_probes.remove('RunningSoftwareProbe')

                if len(missing_probes) == 0: # pylint: disable=len-as-condition
                    cancel_alert(tags=TAG, user_id=device.hash_key)
                else:
                    missing_probes_str = ', '.join(missing_probes[:4])

                    if len(missing_probes) > 4:
                        missing_probes_str = missing_probes_str + ', and ' + str(len(missing_probes) - 4) + ' more'

                    log_alert(message='Missing data from ' + str(len(missing_probes)) + ' probe(s). Absent probes: ' + missing_probes_str, severity=2, tags=TAG, user_id=device.hash_key)
