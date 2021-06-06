from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^work$', views.CreateWorks.as_view()),
    re_path(r'^work/info$', views.HomeListView.as_view()),
    re_path(r'^work/detail/(?P<second_category>\d)$', views.DetailListView.as_view()),
    re_path(r'^work/collection$', views.CollectionView.as_view())
]
