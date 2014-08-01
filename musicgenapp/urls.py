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
	url(r'^rate/(?P<id>[0-9]+)/(?P<rating>[0-9]+)/$', views.rate),
	url(r'^update/(?P<id>[0-9]+)/$', views.updateFiles),
	url(r'^admind/$', views.admin),
	url(r'^admind/songs/(?P<page>[0-9]+)/$', views.adminSongs),
	url(r'^admind/ratings/(?P<page>[0-9]+)/$', views.adminRatings),
	url(r'^admind/users/(?P<page>[0-9]+)/$', views.adminUsers),
	url(r'^song/(?P<id>[0-9]+)/$', views.song),
	url(r'^del/(?P<id>[0-9]+)/$', views.delete),
	url(r'^mut/(?P<id>[0-9]+)/$', views.mutate),
	url(r'^$', views.index),
)