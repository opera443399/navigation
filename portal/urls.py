from django.conf.urls import url
from . import views

app_name = 'portal'
urlpatterns = [
    #################################### /portal/xxx
    #
    url(r'^$', views.show_index, name='show_index'),
    url(r'^show/app/(?P<app_id>[0-9]+)$', views.show_app, name='show_app'),
    url(r'^show/app/default$', views.show_app_default, name='show_app_default'),
    url(r'^show/tree$', views.show_tree, name='show_tree'),

    #################################### /portal/set/xxx
    #
    url(r'^set/default$', views.set_default_app_cat_and_link, name='set_default_app_cat_and_link'),
]