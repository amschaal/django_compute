from django.conf.urls import url
import views

urlpatterns = [
    url(r'^jobs/(?P<job_id>[A-Z0-9]{10})/update/$', views.update_job, name='update_job'),
    url(r'^jobs/(?P<job_id>[A-Z0-9]{10})/run/$', views.run, name='run_job'),
    url(r'^jobs/(?P<job_id>[A-Z0-9]{10})/terminate/$', views.terminate, name='terminate_job'),
    url(r'^jobs/(?P<job_id>[A-Z0-9]{10})/output/(?:(?P<path>.*/))?$', views.job_output, name='job_output'),
]

