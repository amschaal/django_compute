from django.shortcuts import render
import json
from django_compute.models import Job
from django.http.response import JsonResponse
from django_compute.utils import merge
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


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
        job.status = data['status'].upper()
    job.save()
    return JsonResponse({'status':'success'})

@csrf_exempt
@login_required
def run(request,job_id):
    try:
        job = Job.objects.get(id=job_id)
        job.run()
        return JsonResponse({'status':'success'})
    except Exception, e:
        return JsonResponse({'status':'failed','message':str(e.message)},status=400)

@csrf_exempt
@login_required
def terminate(request,job_id):
    try:
        job = Job.objects.get(id=job_id)
        job.terminate()
        return JsonResponse({'status':'success'})
    except Exception, e:
        return JsonResponse({'status':'failed','message':str(e.message)},status=400)
    