from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.authtoken import views as tokenView
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
	url(r'^register/', views.register.as_view(), name='register'),
	url(r'^login/', tokenView.obtain_auth_token),
	url(r'^artque/list/', views.artque_list.as_view(), name='artque-list'),
	url(r'^comment/', views.comment_add.as_view(), name='comment-add'),
	url(r'^discussion/list/', views.discussion_list.as_view(), name='discussion-list'),
)
