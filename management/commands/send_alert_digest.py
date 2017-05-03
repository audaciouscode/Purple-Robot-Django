# pylint: disable=line-too-long, no-member

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template import Context
from django.template.loader import render_to_string

from ...models import PurpleRobotAlert, PurpleRobotDevice


class Command(BaseCommand):
    def handle(self, *args, **options): # pylint: disable=too-many-locals
        group = Group.objects.filter(name=settings.PURPLE_ROBOT_ADMIN_GROUP).first()

        if group is not None:
            users = group.user_set.all()

            recipient_list = []

            for user in users:
                recipient_list.append(user.email)

            alerts = PurpleRobotAlert.objects.filter(dismissed=None).order_by('user_id', '-severity')

            context = Context()
            context['alerts'] = alerts

            if alerts.count() > 0 and recipient_list:
                from_addr = settings.PURPLE_ROBOT_EMAIL_SENDER

                devices = {}

                for alert in alerts:
                    device = PurpleRobotDevice.objects.filter(hash_key=alert.user_id).first()

                    if device is not None:
                        device_alerts = []

                        if device.device_id in devices:
                            device_alerts = devices[device.device_id]
                        else:
                            devices[device.device_id] = device_alerts

                        device_alerts.append([alert, device])

                context['devices'] = devices

                message = render_to_string('email_admin_alert_content.txt', context)
                subject = render_to_string('email_admin_alert_subject.txt', context)

                send_mail(subject, message, from_addr, recipient_list, fail_silently=False)
