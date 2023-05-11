from django import forms
from .models import *
import datetime as dt

class DatePicker(forms.Form):
    date_wig = forms.DateField(
        widget=forms.SelectDateWidget(
            years=[dt.date.today().year]
        ),
        label='Выбрать день для отображения'
    )

