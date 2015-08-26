from django.shortcuts import render
import json, os
from django_compute.models import Job
from django.http.response import JsonResponse
from django_compute.utils import merge, sizeof_fmt
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django_compute.callbacks import get_callback


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
    if data.has_key('output_directory'):
        job.output_directory = data['output_directory']
    job.save()
    if job.callback_id:
        Callback = get_callback(job.callback_id)
        if Callback:
            Callback.run(job=job,data=data)
    return JsonResponse({'status':'success'})

@login_required
def job_output(request,job_id,path):
    path = path if path else ''
    job = Job.objects.get(id=job_id)
    if not job.output_directory:
        raise Exception("This job does not have an output directory specified.")
    if path.count('..') != 0:
        raise Exception("Path may not contain '..'")
    if path.startswith('/'):
        raise Exception("Path may not start with '/'")
    full_path = os.path.join(job.output_directory,path)
    filenames=[]
    directories=[]
    for (dirpath, dirnames, filenames) in os.walk(full_path):
        fileinfo = [{'name':file,'stats':os.stat(os.path.join(full_path,file))} for file in filenames]
        directories=dirnames
        break
#     {'name':file['name'],'size':sizeof_fmt(file['stats'].st_size),'bytes':file['stats'].st_size,'modified':datetime.datetime.fromtimestamp(file['stats'].st_mtime).strftime("%m/%d/%Y %I:%M %p")
    files = [{'name':file['name'], 'size':sizeof_fmt(file['stats'].st_size)} for file in fileinfo]
    return JsonResponse({'job_id':job_id,'path':path,'files':files,'directories':directories})


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
    