# pylint: disable=no-member

import datetime

import arrow
import pytz

from django import template
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone

from ..models import PurpleRobotDeviceGroup, PurpleRobotAlert, PurpleRobotDevice

register = template.Library()


@register.tag(name="pr_device_custom_sidebar")
def pr_device_custom_sidebar(parser, token): # pylint: disable=unused-argument
    return CustomSidebarNode()


class CustomSidebarNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        try:
            return settings.PURPLE_ROBOT_CUSTOM_SIDEBAR(context)
        except AttributeError:
            pass

        return render_to_string('tag_pr_device_custom_sidebar_unknown.html', \
                                context=context.flatten(), request=context.request)


@register.tag(name="pr_device_custom_navbar")
def pr_device_custom_navbar(parser, token): # pylint: disable=unused-argument
    return CustomNavbarNode()


class CustomNavbarNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        try:
            return settings.PURPLE_ROBOT_CUSTOM_NAVBAR(context)
        except AttributeError:
            pass

        return render_to_string('tag_pr_device_custom_navbar_default.html', \
                                context=context.flatten(), request=context.request)

@register.tag(name="pr_home_custom_console")
def tag_pr_home_custom_console(parser, token): # pylint: disable=unused-argument
    return HomeCustomConsoleNode()


class HomeCustomConsoleNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        try:
            return settings.PURPLE_ROBOT_HOME_CONSOLE(context)
        except AttributeError:
            pass

        return render_to_string('tag_pr_home_custom_console_unknown.html', \
                                context=context.flatten(), request=context.request)


@register.tag(name="pr_device_custom_console")
def tag_pr_device_custom_console(parser, token): # pylint: disable=unused-argument
    return DeviceCustomConsoleNode()


class DeviceCustomConsoleNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        try:
            return settings.PURPLE_ROBOT_DEVICE_CONSOLE(context)
        except AttributeError:
            pass

        return render_to_string('tag_pr_device_custom_console_unknown.html', \
                                context=context.flatten(), request=context.request)


@register.tag(name="pr_group_table")
def tag_pr_group_table(parser, token): # pylint: disable=unused-argument
    try:
        tag_name, group_id = token.split_contents() # pylint: disable=unused-variable
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % \
                                           token.contents.split()[0])

    return GroupTableNode(group_id)


class GroupTableNode(template.Node):
    def __init__(self, group_id):
        self.group_id = template.Variable(group_id)

    def render(self, context):
        group_id = self.group_id.resolve(context)

        context['device_group'] = PurpleRobotDeviceGroup.objects.filter(group_id=group_id).first()

        if context['device_group'] != None:
            context['device_group_devices'] = list(context['device_group'].devices.all().order_by('name', 'device_id')) # pylint: disable=line-too-long
        else:
            context['device_group_devices'] = list(PurpleRobotDevice.objects.filter(device_group=None).order_by('name', 'device_id')) # pylint: disable=line-too-long

        return render_to_string('tag_pr_group_table.html', context=context.flatten(), \
                                request=context.request)


@register.tag(name="pr_timestamp_ago")
def tag_pr_timestamp_ago(parser, token): # pylint: disable=unused-argument
    try:
        tag_name, timestamp = token.split_contents() # pylint: disable=unused-variable
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % \
                                           token.contents.split()[0])

    return TimestampAgoNode(timestamp)


class TimestampAgoNode(template.Node):
    def __init__(self, timestamp):
        self.timestamp = template.Variable(timestamp)

    def render(self, context):
        timestamp = self.timestamp.resolve(context)

        date_obj = datetime.datetime.fromtimestamp(int(timestamp) / 1000, pytz.utc)

        if date_obj is None:
            return 'None'

        now = timezone.now()

        diff = arrow.get(now.isoformat()).datetime - arrow.get(date_obj.isoformat()).datetime

        ago_str = 'Unknown'

        if diff.days > 0:
            ago_str = str(diff.days) + 'd'
        else:
            minutes = diff.seconds / 60

            if minutes >= 60:
                ago_str = str(minutes / 60) + 'h'
            else:
                ago_str = str(minutes) + 'm'

        context['ago'] = ago_str
        context['date'] = date_obj

        return render_to_string('tag_pr_date_ago.html', context=context.flatten(), \
                                request=context.request)


@register.tag(name="pr_date_ago")
def tag_pr_date_ago(parser, token): # pylint: disable=unused-argument
    try:
        tag_name, date_obj = token.split_contents() # pylint: disable=unused-variable
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % \
                                           token.contents.split()[0])

    return DateAgoNode(date_obj)


class DateAgoNode(template.Node):
    def __init__(self, date_obj):
        self.date_obj = template.Variable(date_obj)

    def render(self, context):
        date_obj = self.date_obj.resolve(context)

        if date_obj is None:
            return 'None'

        now = timezone.now()

        diff = arrow.get(now.isoformat()).datetime - arrow.get(date_obj.isoformat()).datetime

        ago_str = 'Unknown'

        if diff.days > 0:
            ago_str = str(diff.days) + 'd'
        else:
            minutes = diff.seconds / 60

            if minutes >= 60:
                ago_str = str(minutes / 60) + 'h'
            else:
                ago_str = str(minutes) + 'm'

        context['ago'] = ago_str
        context['date'] = date_obj

        return render_to_string('tag_pr_date_ago.html', context=context.flatten(), \
                                request=context.request)


@register.tag(name="pr_human_duration")
def tag_pr_human_duration(parser, token): # pylint: disable=unused-argument
    try:
        tag_name, seconds_obj = token.split_contents() # pylint: disable=unused-variable
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % \
                                           token.contents.split()[0])

    return HumanDurationNode(seconds_obj)


class HumanDurationNode(template.Node):
    def __init__(self, seconds_obj):
        self.seconds_obj = template.Variable(seconds_obj)

    def render(self, context):
        seconds_obj = self.seconds_obj.resolve(context)

        if seconds_obj is None:
            return ''

        ago_str = str(seconds_obj) + 's'

        if seconds_obj > (24.0 * 60 * 60):
            ago_str = "{0:.2f}".format(seconds_obj / (24.0 * 60 * 60)) + 'd'
        elif seconds_obj > (60.0 * 60):
            ago_str = "{0:.2f}".format(seconds_obj / (60.0 * 60)) + 'h'
        elif seconds_obj > 60.0:
            ago_str = "{0:.2f}".format(seconds_obj / 60.0) + 'm'

        context['human_duration'] = ago_str
        context['seconds'] = seconds_obj

        return render_to_string('tag_pr_human_duration.html', context=context.flatten(), \
                                request=context.request)


@register.tag(name="pr_frequency")
def tag_pr_frequency(parser, token): # pylint: disable=unused-argument
    try:
        tag_name, frequency = token.split_contents() # pylint: disable=unused-variable
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % \
                                           token.contents.split()[0])

    return FrequencyNode(frequency)


class FrequencyNode(template.Node):
    def __init__(self, frequency):
        self.frequency = template.Variable(frequency)

    def render(self, context):
        frequency = self.frequency.resolve(context)

        if frequency is None:
            return 'None'
        elif frequency == 'Unknown':
            return frequency

        value = "{:10.3f}".format(frequency) + " Hz"

        if frequency < 1.0:
            value = "{:10.3f}".format(frequency * 1000) + " mHz"

        tooltip = "{:10.3f}".format(frequency) + " samples per second"

        if frequency < 1.0:
            frequency *= 60

            if frequency > 1.0:
                tooltip = "{:10.3f}".format(frequency) + " samples per minute"
            else:
                frequency *= 60

                if frequency > 1.0:
                    tooltip = "{:10.3f}".format(frequency) + " samples per hour"
                else:
                    frequency *= 24

                    if frequency > 1.0:
                        tooltip = "{:10.3f}".format(frequency) + " samples per day"
                    else:
                        frequency *= 7

                        tooltip = "{:10.3f}".format(frequency) + " samples per week"

        context['value'] = value
        context['tooltip'] = tooltip

        return render_to_string('tag_pr_frequency.html', context=context.flatten(), \
                                request=context.request)


@register.tag(name="pr_device_alerts")
def tag_pr_device_alerts(parser, token): # pylint: disable=unused-argument
    try:
        tag_name, user_id = token.split_contents() # pylint: disable=unused-variable
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % \
                                           token.contents.split()[0])

    return DeviceAlertsNode(user_id)


class DeviceAlertsNode(template.Node):
    def __init__(self, user_id):
        self.user_id = template.Variable(user_id)

    def render(self, context):
        user_id = self.user_id.resolve(context)

        device = PurpleRobotDevice.objects.filter(hash_key=user_id).first()

        if device is not None and device.mute_alerts:
            context['class'] = ''
            context['value'] = 0
            context['tooltip'] = 'No alerts.'

            return render_to_string('tag_pr_device_alerts.html', context=context.flatten(), \
                                    request=context.request)

        alerts = PurpleRobotAlert.objects.filter(user_id=user_id, dismissed=None).order_by('-severity')  # pylint: disable=line-too-long

        tooltip = 'No alerts.'

        severity = 0

        if alerts.count() > 0:
            tooltip = ''

            for alert in alerts:
                if tooltip:
                    tooltip += '\n'

                tooltip += alert.message

                if alert.severity > severity:
                    severity = alert.severity

        if severity > 1:
            context['class'] = 'text-danger'
        elif severity > 0:
            context['class'] = 'text-warning'
        else:
            context['class'] = ''

        context['value'] = alerts.count()
        context['tooltip'] = tooltip

        return render_to_string('tag_pr_device_alerts.html', context=context.flatten(), \
                                request=context.request)


@register.tag(name="pr_data_size")
def tag_pr_data_size(parser, token): # pylint: disable=unused-argument
    try:
        tag_name, data_size = token.split_contents() # pylint: disable=unused-variable
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % \
                                           token.contents.split()[0])

    return DataSizeNode(data_size)


class DataSizeNode(template.Node):
    def __init__(self, data_size):
        self.data_size = template.Variable(data_size)

    def render(self, context):
        size = self.data_size.resolve(context)

        if size is None:
            size = 0

        data_size = float(size)

        if data_size < 0:
            return 'Unknown / None'

        if data_size > (1024 * 1024 * 1024):
            return "{:10.1f}".format(data_size / (1024 * 1024 * 1024)) + " GB"
        elif data_size > (1024 * 1024):
            return "{:10.1f}".format(data_size / (1024 * 1024)) + " MB"
        elif data_size > 1024:
            return "{:10.1f}".format(data_size / 1024) + " KB"

        return str(data_size) + " B"


@register.filter(name='to_percent')
def to_percent(value):
    return value * 100


@register.tag(name="pr_total_data_size")
def tag_pr_total_database_size(parser, token): # pylint: disable=unused-argument
    return TotalDataSizeNode()


class TotalDataSizeNode(template.Node):
    def render(self, context):
        data_size = 0

        for device in PurpleRobotDevice.objects.all():
            size = device.total_readings_size()

            if size is None:
                size = 0

            data_size += size

        data_size *= 2

        if data_size <= 0:
            return 'Unknown / None'

        if data_size > (1024 * 1024 * 1024):
            return "{:10.1f}".format(data_size / (1024 * 1024 * 1024)) + " GB"
        elif data_size > (1024 * 1024):
            return "{:10.1f}".format(data_size / (1024 * 1024)) + " MB"
        elif data_size > 1024:
            return "{:10.1f}".format(data_size / 1024) + " KB"

        return str(data_size) + " B"
