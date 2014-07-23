from django.conf.urls import patterns, url

from musicgenapp import views

urlpatterns = patterns('',
	#url(r'^(?P<course_id>[0-9]+)/$', views.courseDetails),
	url(r'^about/$', views.about),
	url(r'^$', views.index),
)