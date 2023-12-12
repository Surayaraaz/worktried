from django.urls import include, re_path
from ehrms import Employviews,adminviews

app_name = 'ehrms'
urlpatterns = [

    re_path(r'^calendar/$', Employviews.CalendarView.as_view(), name='calendar'),
    re_path('employ_apply_leave/', Employviews.employ_apply_leave, name='employ_apply_leave'),
    re_path(r'^calendar1/$', adminviews.CalendarView_1.as_view(), name='calendar1'),


]