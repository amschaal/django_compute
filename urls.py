from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^job/(?P<job_id>[A-Z0-9]{10})/update/$', 'django_compute.views.update_job', name='update_job'),
)

