
from django.contrib import admin
from django.urls import path, include
from .views import ( 
    EmployeeView, show_employee_exits,
    ExitView,
    CenterView, ReviewView
)
urlpatterns = [
    #----------------------employee-----------------------------------
    path('employees/', EmployeeView.as_view(), name='employee-views'),
    path('employees/<str:uuid>', EmployeeView.as_view(), name='employee-details-views'),
    path('employees/exits/<str:uuid>', show_employee_exits, name='showEmployeeExits'),
    #----------------------Exit----------------------------------------
    path('exits/', ExitView.as_view(), name='exit-views'),
    path('exits/<str:uuid>', ExitView.as_view(), name='exit-details-views'),
    #----------------------Center--------------------------------------
    path('centers/', CenterView.as_view(), name='center-views'),
    path('centers/<str:uuid>', CenterView.as_view()),
    path('centers/reviews/<str:center_uuid>', ReviewView.as_view(), name='review-views'),
    path('centers/reviews/<str:center_uuid>/<str:uuid>', ReviewView.as_view(), name='add-review'),
]