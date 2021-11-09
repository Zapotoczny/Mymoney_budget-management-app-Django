from django.urls import path, include
from . import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(),name='login'),
    path('app', views.index, name='index'),
    # path('chart', views.chart, name='chart'),
    path('charts', views.charts, name='charts'),
    path('settings', views.settings, name='settings'),
    path('raports', views.raports, name='raports'),
    path('export_xls', views.export_xls, name='export_xls'),
    path('export_pdf', views.export_pdf, name='export_pdf'),
    path('operations', views.operations, name='operations'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('payments', views.payments, name='payments'),
    path('add_payment', views.add_payment, name='add payment'),
    path('signup/', views.signup, name='signup'),
    path('add_item', views.add_item, name='add item'),
    path(r'^delete_item/(?P<pk>\d+)$', views.delete_item, name='delete item'),
    path(r'^delete_item_calendar/(?P<pk>\d+)$', views.delete_item_calendar, name='delete item calendar'),
    path(r'^show_payments/(?P<pk>\d+)$', views.show_payments, name='show payments'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('logout', views.logout_view, name='logout'),
]