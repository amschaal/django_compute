from django.shortcuts import render
import json
from django_compute.models import Job
from django.http.response import JsonResponse
from django_compute.utils import merge
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def update_job(request,job_id):
    api_key = request.GET.get('api_key')
    job = Job.objects.get(id=job_id,api_key=api_key)
    data =json.loads(request.body)
    print data
    #callback(job.callback,job=job,data=data)
    if data.has_key('data'):
        job.data = merge(job.data,data['data'])
    if data.has_key('status'):
        job.status = data['status']
    job.save()
    return JsonResponse({'status':'success'})
    