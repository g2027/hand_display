from django.contrib import admin
from django.urls import include, path
from basic import views
urlpatterns = [
    path("", views.medidata_get_view),
    path("basic/create/", views.create_rawdata),
   
]
