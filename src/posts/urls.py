from django.conf.urls import url
from django.contrib import admin

from posts.views import post_list,post_create,post_detail,post_update,post_delete
	

urlpatterns = [
    
    url(r'^$', post_list,name='list'),
    url(r'^create/$', post_create),
    url(r'^(?P<id>\d+)/$', post_detail, name='detail'),#for detail
    url(r'^(?P<id>\d+)/edit/$', post_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', post_delete),
    #url(r'^posts/$', "<appName>.views.<functionName>"),
]
