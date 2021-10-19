from datetime import datetime, timedelta, date
from calendar import HTMLCalendar
from .models import Event, ExpenseInfo
from django.db.models import Sum


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        # events_per_day = events.filter(start_time__day=day)
        d = ExpenseInfo.objects.filter(date_added__day=day).aggregate(
            budget=Sum('cost'))
        print(type(d['budget']))
        if type(d['budget']) is float:
            if d['budget'] < 0:
                color = 'red'
            else:
                color = 'green'
        else:
            color = 'white'
        # for event in events_per_day:
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul style='color:{color};'><b> {d['budget']} </b></ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal
