from django.urls import re_path
from . import views


urlpatterns = [
    re_path('^username/(?P<username>\w{3,20})/count$', views.UsernameCountView.as_view()),
    re_path('^mobiles/(?P<mobile>1[3-9]\d{9})/count$', views.MobileCountView.as_view()),
    re_path(r'^register$', views.RegisterView.as_view()),
    re_path(r'^login$', views.LoginView.as_view()),
    re_path(r'^logout$', views.LogoutView.as_view()),
    re_path(r'^user/(?P<user_id>\d)$', views.UserInfoView.as_view()),
    re_path(r'^user/works/(?P<user_id>\d)$', views.UserWorks.as_view()),
]
