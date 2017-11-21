
from django.conf.urls import include,url
from django.contrib import admin

urlpatterns = [
    url(r'^plant/', include('plant.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('plant.urls'),name="plant")
]

