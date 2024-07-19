from django.urls import path, re_path
from .views import (
    CustomTokenObtainPairView,
      CustomTokenRefreshView, 
      CustomTokenVerifyView, 
      LogoutView, 
      CustomProviderAuthView, 
      CompleteUserView,
      ManagerViewRegistration
)
urlpatterns = [
    re_path(
        r'^o/(?P<provider>\S+)/$',
        CustomProviderAuthView.as_view(),
        name='provider-auth',
    ),
    path('jwt/create', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh', CustomTokenRefreshView.as_view()),
    path('jwt/verify', CustomTokenVerifyView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('complete/', CompleteUserView.as_view()),
    path('users/manager', ManagerViewRegistration.as_view()),
]