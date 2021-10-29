from django.http import HttpResponse
from django.template import loader
from back.models import Task, SubTask

# Create your views here.

def tasks(request):
    tasks = Task.objects.all()
    template = loader.get_template('client/task.html')
    context = {'tasks': tasks,}
    return HttpResponse(template.render(context, request))

def subtasks(request):
    subtasks = SubTask.objects.all()
    template = loader.get_template('client/subtask.html')
    context = {'subtasks': subtasks,}
    return HttpResponse(template.render(context, request))