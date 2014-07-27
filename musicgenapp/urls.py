from django.conf.urls import patterns, url

from musicgenapp import views

urlpatterns = patterns('',
	#url(r'^(?P<course_id>[0-9]+)/$', views.courseDetails),
	url(r'^about/$', views.about),
	url(r'^signup/$', views.signup),
	url(r'^login/$', views.login),
	url(r'^list/$', views.list),
	url(r'^forgot/$', views.forgot),
	url(r'^account/$', views.account),
	url(r'^logout/$', views.logout),
	url(r'^reset/$', views.reset),
	url(r'^random/$', views.random),
	url(r'^rate/$', views.rate),
	url(r'^update/$', views.updateFiles),
	url(r'^$', views.index),
)