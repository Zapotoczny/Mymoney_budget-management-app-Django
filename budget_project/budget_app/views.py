import calendar
from datetime import date, timedelta
from collections import Counter

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q, Count
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .forms import SignUpForm, LoginForm

from .models import ExpenseInfo, Event
from .utils import Calendar
# Create your views here.
from datetime import datetime
from django.views import generic
from django.utils.safestring import mark_safe


class CalendarView(generic.ListView):
    model = Event
    template_name = 'budget_app/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month



def index(request):
    budget_id = request.user.last_name
    username = ExpenseInfo.username
    expense_items = ExpenseInfo.objects.filter(user_expense=budget_id).order_by('-date_added')[:5]
    try:
        budget_total = ExpenseInfo.objects.filter(user_expense=budget_id).aggregate(
            budget=Sum('cost', filter=Q(cost__gt=0)))
        expense_total = ExpenseInfo.objects.filter(user_expense=budget_id).aggregate(
            expenses=Sum('cost', filter=Q(cost__lt=0)) * -1)
        expense_today = ExpenseInfo.objects.filter(user_expense=budget_id, date_added=date.today()).aggregate(
            expenses=Sum('cost', filter=Q(cost__lt=0)) * -1)
        expense_month = ExpenseInfo.objects.filter(user_expense=budget_id,
                                                   date_added__month=date.today().month).aggregate(
            expenses=Sum('cost', filter=Q(cost__lt=0)) * -1)
        if expense_total['expenses'] is not None:
            balance = budget_total['budget'] - expense_total['expenses']
        else:
            balance = budget_total['budget']
    except TypeError or UnboundLocalError:
        print('No data.')

    # Wykres wydatków

    labels = []
    data = []
    for x in range(7):
        dzien = date.today() - timedelta(days=x)
        dzien = dzien.strftime("%Y-%m-%d")
        labels.append(dzien)
        dupa = ExpenseInfo.objects.filter(date_added=labels[x]).aggregate(
            expenses=Sum('cost', filter=Q(cost__lt=0)) * -1)
        if dupa['expenses'] is None:
            dupa['expenses'] = 0
        data.append(dupa['expenses'])

    context = {'username': username, 'expense_items': expense_items, 'budget': budget_total['budget'],
               'expenses': expense_total['expenses'], 'expenses_today': expense_today['expenses'],
               'expenses_month': expense_month['expenses'], 'balance': balance, 'labels': labels, 'data': data}
    return render(request, 'budget_app/index.html', context=context)


def add_item(request):
    budget_id = request.user.last_name
    name = request.POST['expense_name']
    category = request.POST['category']
    expense_cost = request.POST['cost']
    expense_date = request.POST['expense_date']
    try:
        ExpenseInfo.objects.create(username=request.user, expense_name=name, category=category, cost='-' + expense_cost,
                                   date_added=expense_date, user_expense=budget_id)
    except ValueError or TypeError:
        print('No data.')
    return HttpResponseRedirect('app')


def delete_item(request, pk):
    ExpenseInfo.objects.filter(id=pk).delete()
    return HttpResponseRedirect('/app')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def settings(request):
    return render(request, "budget_app/settings.html")


def operations(request):
    try:
        from_ = request.POST['from']
        to_ = request.POST['to']
    except:
        to_, from_ = date.today(), date.today() - timedelta(days=7)
    budget_id = request.user.last_name
    expense_items = ExpenseInfo.objects.filter(user_expense=budget_id, date_added__range=[from_, to_]).order_by(
        '-date_added')
    balance = ExpenseInfo.objects.filter(user_expense=budget_id, date_added__month=date.today().month).aggregate(
        budget=Sum('cost'))
    balance_month = ExpenseInfo.objects.filter(user_expense=budget_id,
                                               date_added__month=date.today().month - 1).aggregate(
        budget=Sum('cost'))
    context = {'expense_items': expense_items,
               'balance': balance['budget'],
               'balance_month': balance_month['budget']}
    return render(request, "budget_app/operations.html", context=context)


def calendar_payment(request):
    return render(request, "budget_app/calendar.html")


def charts(request):
    budget_id = request.user.last_name
    #################################################
    # Week
    #################################################
    labels = []
    labels2 = []
    data = []
    data_user1 = []
    data_user2 = []

    user2 = list(User.objects.filter(last_name=budget_id))
    user2.remove(request.user)
    user2_name = user2[0]

    for x in range(7):
        dzien = date.today() - timedelta(days=x)
        dzien = dzien.strftime("%Y-%m-%d")
        labels.insert(0, dzien)
        labels2.append(dzien)

        dupa = ExpenseInfo.objects.filter(date_added=labels2[x], user_expense=budget_id).aggregate(
            expenses=Sum('cost', filter=Q(cost__lt=0)) * -1)

        user1 = ExpenseInfo.objects.filter(date_added=labels2[x], user_expense=budget_id,
                                           username=request.user).aggregate(
            expenses=Sum('cost', filter=Q(cost__lt=0)) * -1)

        user2 = ExpenseInfo.objects.filter(date_added=labels2[x], user_expense=budget_id,
                                           username=user2_name).aggregate(
            expenses=Sum('cost', filter=Q(cost__lt=0)) * -1)

        if dupa['expenses'] is None:
            dupa['expenses'] = 0
        if user1['expenses'] is None:
            user1['expenses'] = 0
        if user2['expenses'] is None:
            user2['expenses'] = 0
        data.insert(0, dupa['expenses'])
        data_user1.insert(0, user1['expenses'])
        data_user2.insert(0, user2['expenses'])
    #################################################
    # Month
    #################################################
    labels_month = []
    labels2_month = []
    data_month = []
    data_month_user1 = []
    data_month_user2 = []
    for x in range(30):
        dzien_month = date.today() - timedelta(days=x)
        dzien_month = dzien_month.strftime("%Y-%m-%d")
        labels2_month.append(dzien_month)
        labels_month.insert(0, dzien_month)
        dupa_month = ExpenseInfo.objects.filter(date_added=labels2_month[x], user_expense=budget_id).aggregate(
            expenses=Sum('cost', filter=Q(cost__lt=0)) * -1)

        user1 = ExpenseInfo.objects.filter(date_added=labels2_month[x], user_expense=budget_id,
                                           username=request.user).aggregate(
            expenses=Sum('cost', filter=Q(cost__lt=0)) * -1)

        user2 = ExpenseInfo.objects.filter(date_added=labels2_month[x], user_expense=budget_id,
                                           username=user2_name).aggregate(
            expenses=Sum('cost', filter=Q(cost__lt=0)) * -1)

        if dupa_month['expenses'] is None:
            dupa_month['expenses'] = 0
        if user1['expenses'] is None:
            user1['expenses'] = 0
        if user2['expenses'] is None:
            user2['expenses'] = 0
        data_month.insert(0, dupa_month['expenses'])
        data_month_user1.insert(0, user1['expenses'])
        data_month_user2.insert(0, user2['expenses'])
    #################################################
    # Year and payments
    #################################################
    labels_year = []
    data_year = []
    data_year_user1 = []
    data_year_user2 = []
    data_payments_user1 = []
    data_payments_user2 = []
    data_payments_all = []
    previous_year = 0
    for x in range(12):
        if x >= date.today().month:
            x += -12
            previous_year = 1

        dupa_test = ExpenseInfo.objects.filter(user_expense=budget_id,
                                               date_added__month=date.today().month - x,
                                               date_added__year=date.today().year - previous_year).aggregate(
            expenses=Sum('cost', filter=Q(cost__lt=0)) * -1)
        user1 = ExpenseInfo.objects.filter(user_expense=budget_id,
                                           date_added__month=date.today().month - x,
                                           date_added__year=date.today().year - previous_year,
                                           username=request.user).aggregate(
            expenses=Sum('cost', filter=Q(cost__lt=0)) * -1)
        user2 = ExpenseInfo.objects.filter(user_expense=budget_id,
                                           date_added__month=date.today().month - x,
                                           date_added__year=date.today().year - previous_year,
                                           username=user2_name).aggregate(
            expenses=Sum('cost', filter=Q(cost__lt=0)) * -1)
        payments_all = ExpenseInfo.objects.filter(user_expense=budget_id,
                                                  date_added__month=date.today().month - x,
                                                  date_added__year=date.today().year - previous_year).aggregate(
            expenses=Sum('cost', filter=Q(cost__gt=0)))
        user1_payments = ExpenseInfo.objects.filter(user_expense=budget_id,
                                                    date_added__month=date.today().month - x,
                                                    date_added__year=date.today().year - previous_year,
                                                    username=request.user).aggregate(
            expenses=Sum('cost', filter=Q(cost__gt=0)))
        user2_payments = ExpenseInfo.objects.filter(user_expense=budget_id,
                                                    date_added__month=date.today().month - x,
                                                    date_added__year=date.today().year - previous_year,
                                                    username=user2_name).aggregate(
            expenses=Sum('cost', filter=Q(cost__gt=0)))
        if dupa_test['expenses'] is None:
            dupa_test['expenses'] = 0
        if user1['expenses'] is None:
            user1['expenses'] = 0
        if user2['expenses'] is None:
            user2['expenses'] = 0
        if payments_all['expenses'] is None:
            payments_all['expenses'] = 0
        if user1_payments['expenses'] is None:
            user1_payments['expenses'] = 0
        if user2_payments['expenses'] is None:
            user2_payments['expenses'] = 0
        data_year.insert(0, dupa_test['expenses'])
        labels_year.insert(0, calendar.month_name[date.today().month - x])
        data_year_user1.insert(0, user1['expenses'])
        data_year_user2.insert(0, user2['expenses'])
        data_payments_user1.insert(0, user1_payments['expenses'])
        data_payments_user2.insert(0, user2_payments['expenses'])
        data_payments_all.insert(0, payments_all['expenses'])
    #################################################
    # Category
    #################################################
    payments_category = ['Nagroda', 'Wypłata', 'Inne']
    labels_category = []
    data_category = []
    category = ExpenseInfo.objects.values('category').order_by('category').annotate(count=Count('category'))
    for x in range(len(category)):
        if category[x].get('category') not in payments_category:
            labels_category.append(category[x].get('category'))
            data_category.append(category[x].get('count'))
    #################################################
    # Category expanse
    #################################################
    category_exp = ExpenseInfo.objects.values('cost', 'category').order_by('category')
    test = {}
    for x in category_exp:
        if x.get('cost') < 0:
            if x.get('category') in test:
                test[x.get('category')] += x.get('cost') * -1
            else:
                test[x.get('category')] = x.get('cost') * -1
    labels_category_exp = list(test.keys())
    data_category_exp = list(test.values())

    #################################################
    # Payments last year
    #################################################
    expense_payments_user1 = ExpenseInfo.objects.filter(user_expense=budget_id,
                                                        date_added__year=date.today().year,
                                                        username=user2_name).aggregate(
        expenses=Sum('cost', filter=Q(cost__gt=0)))
    expense_payments_user2 = ExpenseInfo.objects.filter(user_expense=budget_id,
                                                        date_added__year=date.today().year,
                                                        username=request.user).aggregate(
        expenses=Sum('cost', filter=Q(cost__gt=0)))

    #################################################
    # context
    #################################################
    context = {'labels': labels,
               'data': data,
               'data_user1': data_user1,
               'data_user2': data_user2,
               'user1': request.user,
               'user2_name': user2_name,
               'labels_month': labels_month,
               'data_month': data_month,
               'data_month_user1': data_month_user1,
               'data_month_user2': data_month_user2,
               'labels_year': labels_year,
               'data_year': data_year,
               'data_year_user1': data_year_user1,
               'data_year_user2': data_year_user2,
               'labels_category': labels_category,
               'data_category': data_category,
               'labels_category_exp': labels_category_exp,
               'data_category_exp': data_category_exp,
               'expense_payments_user1': expense_payments_user1['expenses'],
               'expense_payments_user2': expense_payments_user2['expenses'],
               'data_payments_user1': data_payments_user1,
               'data_payments_user2': data_payments_user2,
               'data_payments_all': data_payments_all}
    return render(request, "budget_app/charts.html", context)


def add_payment(request):
    budget_id = request.user.last_name
    name = request.POST['payment_name']
    category = request.POST['category']
    expense_cost = request.POST['cost']
    expense_date = request.POST['payment_date']
    try:
        ExpenseInfo.objects.create(username=request.user, expense_name=name, category=category, cost=expense_cost,
                                   date_added=expense_date, user_expense=budget_id)
    except ValueError or TypeError:
        print('No data.')
    return HttpResponseRedirect('payments')


def payments(request):
    budget_id = request.user.last_name
    try:
        expense_items = ExpenseInfo.objects.filter(user_expense=budget_id, cost__gte=0).order_by('-date_added')[:5]
        expense_month = ExpenseInfo.objects.filter(user_expense=budget_id,
                                                   date_added__month=date.today().month).aggregate(
            expenses=Sum('cost', filter=Q(cost__gt=0)))
        expense_month_last = ExpenseInfo.objects.filter(user_expense=budget_id,
                                                        date_added__month=date.today().month - 1).aggregate(
            expenses=Sum('cost', filter=Q(cost__gt=0)))
    except TypeError or UnboundLocalError:
        print('No data.')
    contex = {'expense_items': expense_items,
              'expense_month': expense_month['expenses'],
              'expense_month_last': expense_month_last['expenses']}
    return render(request, 'budget_app/payments.html', contex)


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            form.save()
            new_user = authenticate(username=username, password=password)
            if new_user is not None:
                signup(request)
                login(request, new_user)
                return HttpResponseRedirect('/app')
        else:
            context = {'form': form, 'error': ''}
            return render(request, 'budget_app/signup.html', context)
    form = SignUpForm()

    context = {'form': form}
    return render(request, "budget_app/signup.html", context)
