from django import forms
from django.contrib.admin.widgets import AdminDateWidget
import datetime


# === Custom Time Widgets ===

class AMPMTimeWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.Select(attrs=attrs, choices=[(str(i), f"{i:02d}") for i in range(1, 13)]),
            forms.Select(attrs=attrs, choices=[(str(i), f"{i:02d}") for i in range(0, 60)]),
            forms.Select(attrs=attrs, choices=[('AM', 'AM'), ('PM', 'PM')]),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            if isinstance(value, str):
                t = datetime.datetime.strptime(value, '%H:%M:%S').time()
            else:
                t = value
            hour = t.hour
            minute = t.minute
            ampm = 'AM'
            if hour == 0:
                hour = 12
            elif hour == 12:
                ampm = 'PM'
            elif hour > 12:
                hour -= 12
                ampm = 'PM'
            return [str(hour), str(minute), ampm]
        return [None, None, None]


class AMPMTimeField(forms.MultiValueField):
    widget = AMPMTimeWidget

    def __init__(self, *args, **kwargs):
        fields = [
            forms.ChoiceField(choices=[(str(i), f"{i:02d}") for i in range(1, 13)]),
            forms.ChoiceField(choices=[(str(i), f"{i:02d}") for i in range(0, 60)]),
            forms.ChoiceField(choices=[('AM', 'AM'), ('PM', 'PM')]),
        ]
        super().__init__(fields, require_all_fields=True, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            hour = int(data_list[0])
            minute = int(data_list[1])
            ampm = data_list[2]
            if ampm == 'PM' and hour != 12:
                hour += 12
            elif ampm == 'AM' and hour == 12:
                hour = 0
            return datetime.time(hour, minute)
        return None


class AdminSplitDateTimeAMPMWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            AdminDateWidget(attrs=attrs),
            AMPMTimeWidget(attrs=attrs),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            if isinstance(value, str):
                dt = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            else:
                dt = value
            return [dt.date(), dt.time()]
        return [None, None]


class SplitDateTimeAMPMField(forms.MultiValueField):
    widget = AdminSplitDateTimeAMPMWidget

    def __init__(self, *args, **kwargs):
        fields = [
            forms.DateField(),
            AMPMTimeField(),
        ]
        super().__init__(fields, require_all_fields=True, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            if data_list[0] is None or data_list[1] is None:
                return None
            return datetime.datetime.combine(data_list[0], data_list[1])
        return None