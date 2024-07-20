
from django.contrib import admin
from django.urls import path, include
from .views import ( 
    EmployeeView, show_employee_exits,
    ExitView,
    CenterView, show_reviews, add_review
)
urlpatterns = [
    #----------------------employee-----------------------------------
    path('employees/', EmployeeView.as_view()),
    path('employees/<str:uuid>', EmployeeView.as_view()),
    path('employees/exits/<str:uuid>', show_employee_exits, name='showEmployeeExits'),
    #----------------------Exit----------------------------------------
    path('exits/', ExitView.as_view()),
    path('exits/<str:uuid>', ExitView.as_view()),
    #----------------------Center--------------------------------------
    path('centers/', CenterView.as_view()),
    path('centers/<str:uuid>', CenterView.as_view()),
    path('centers/reviews/<str:center_uuid>', show_reviews, name='showReviewListOfCenter'),
    path('centers/reviews/<str:center_uuid>', add_review, name='addReviewOfCenter'),
]