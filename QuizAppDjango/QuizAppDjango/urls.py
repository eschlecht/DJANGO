from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.homepage, name='homepage'),
    url(r'^quiz/', include('quiz.urls')),
    url(r'^account/', include('account.urls')),


]
