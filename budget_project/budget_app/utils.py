from calendar import HTMLCalendar
from .models import ExpenseInfo
from django.db.models import Sum
from django.contrib.auth.models import User


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None,):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day):
        # budget_id = request.user.budget_id
        current_date = f'{self.year}-{self.month}-{day}'
        d = ExpenseInfo.objects.filter(date_added__day=day, date_added__month=self.month,
                                       date_added__year=self.year).aggregate(
            budget=Sum('cost'))
        if type(d['budget']) is float:
            if d['budget'] < 0:
                color = 'red'
                up_down = "src='https://i.ibb.co/6BQ78rD/down.png'"
            else:
                color = 'green'
                up_down = "src='https://i.ibb.co/QPFBvYq/up.png'"
        else:
            color = 'white'
            up_down = "src='https://www.colorhexa.com/ffffff.png'"
        # for event in events_per_day:
        if day != 0:
            return """<td class='cell'>
            <a href="/%5Eshow_payments/(%3FP{}%5Cd+)$">
            <div style="height:100%;width:100%">
            <span class='date'>{}</span>
            <ul class='date_month' style='color:{};'><b> {} </b>
            <img {} width='20' height='24'>
            </ul></td></a></div>""".format(current_date, day, color, d['budget'], up_down)
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week)}\n'
        return cal
