from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'upload/img$', views.UploadImage.as_view())
]
