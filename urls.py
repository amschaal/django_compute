from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^jobs/(?P<job_id>[A-Z0-9]{10})/update/$', 'django_compute.views.update_job', name='update_job'),
    url(r'^jobs/(?P<job_id>[A-Z0-9]{10})/run/$', 'django_compute.views.run', name='run_job'),
    url(r'^jobs/(?P<job_id>[A-Z0-9]{10})/terminate/$', 'django_compute.views.terminate', name='terminate_job'),
    url(r'^jobs/(?P<job_id>[A-Z0-9]{10})/output/(?:(?P<path>.*/))?$', 'django_compute.views.job_output', name='job_output'),
)

