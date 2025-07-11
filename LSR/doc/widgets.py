from django import forms
from datetime import date


class CustomDatePickerWidget(forms.DateInput):
    """
    A custom date picker widget that uses HTML5 date input type.
    """
    DATE_INPUT_WIDGET_REQUIRED_FORMAT = "%Y-%m-%d"

    def __init__(self, attrs={}, format=None):
        attrs.update(
            {
                'class': 'form-control',
                'type': 'date',
            }
        )
        self.format = format or self.DATE_INPUT_WIDGET_REQUIRED_FORMAT
        super().__init__(attrs, format=self.format)


class PastCustomDatePickerWidget(CustomDatePickerWidget):
    """
    A custom date picker widget that only allows past dates.
    """

    def __init__(self, attrs={}, format=None):
        attrs.update({'max': date.today()})
        super().__init__(attrs, format=format)
