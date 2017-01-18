from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views


app_name = 'account'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', auth_views.login, {'template_name': 'account/login.html'}, name='login'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^registration/$', views.UserRegistration.as_view(), name='registration'),
    url(r'^profile/$', views.profile, name ='profile'),
    url(r'^update_account/$', views.update_account, name='update_account'),
    url(r'^update_picture/$', views.update_picture, name='update_picture'),
    url(r'^update_picture/(?P<profilepicture_id>[0-9]+)/$', views.update_picture_save, name='update_picture_save'),
    url(r'^course_statistic/$', views.course_statistic, name='course_statistic'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
