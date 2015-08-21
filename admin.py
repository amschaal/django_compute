from django.contrib import admin
from django_compute.models import Job, JobTemplate
# Register your models here.
class JobTemplateAdmin(admin.ModelAdmin):
    model = JobTemplate
class JobAdmin(admin.ModelAdmin):
    model = Job

admin.site.register(JobTemplate, JobTemplateAdmin)
admin.site.register(Job, JobAdmin)