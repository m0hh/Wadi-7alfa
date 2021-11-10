from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from back.models import Task, SubTask, UserInfo
from django.shortcuts import render
from .forms import ClientForm
import requests
from django.urls import reverse

# Create your views here.

def tasks(request):
    tasks = Task.objects.filter(user = request.user.info)
    template = loader.get_template('client/task.html')
    context = {'tasks': tasks,}
    return HttpResponse(template.render(context, request))

def subtasks(request):
    subtasks = SubTask.objects.filter(user = request.user.info)
    template = loader.get_template('client/subtask.html')
    context = {'subtasks': subtasks,}
    return HttpResponse(template.render(context, request))

def index(request):
    return render(request, 'client/index.html')

def sync(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            data = createweb(form.cleaned_data['api_pk'], form.cleaned_data['team_id'])
            if 'webhook' in data.keys():
                UserInfo.objects.create(api_pk = data['webhook']['client_id'],
                team_id = data['webhook']['team_id'], user = request.user,
                name = form.cleaned_data['your_name'], 
                site_id = data['webhook']['userid'], webhook_id = data['id'])

                return HttpResponseRedirect(reverse('home'))
            
            else:
                return render(request, 'client/sync.html', {'form': form ,'message': 'You entered wrong credentials'})

    else:
        form = ClientForm()
    
    return render(request, 'client/sync.html', {'form': form})

def createweb(token, t_id):
    values = {
        "endpoint": "https://ee29-156-208-73-34.ngrok.io/task/",
        "events": [
        "taskCreated",
        "taskUpdated",
        "taskDeleted",
        "taskTimeTrackedUpdated",
        "listCreated",
        "listUpdated",
        "listDeleted",
        "spaceCreated",
        "spaceUpdated",
        "spaceDeleted",
        ]
    }

    header = {
    'Authorization': token,
    'Content-Type': 'application/json'
    }
    r = requests.post(f'https://api.clickup.com/api/v2/team/{t_id}/webhook', headers=header, json=values)
    return r.json()

