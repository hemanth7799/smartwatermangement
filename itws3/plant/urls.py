from django.conf.urls import include,url
from . import views
app_name='plant'
urlpatterns = [
    url(r'^$', views.home ,name = "home") ,
    url(r'^get/$', views.getdata ,name ="get"),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^dashboard/(?P<plantid>[0-9]+)/$', views.newdashboard, name='newdashboard'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^map/(?P<plantid>[0-9]+)/$', views.newmap, name='newmap'),
    url(r'^map/$', views.map, name='map'),
    url(r'^motorcontrol/$', views.actuatorcontrol, name='mcontrol'),
    url(r'^add/$', views.add ,name ="add"),
    url(r'^addPlant/$', views.addPlant ,name ="addPlant"),

]
