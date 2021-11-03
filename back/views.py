from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from .models import Task, SubTask, UserInfo



@api_view(['POST'])
def Clickup(request):
    if request.method == "POST":
        data = dict(request.data)
        print(data)
        request_router(data)
        return Response(status='200')



def request_router(data):
    id = data['task_id']
    if data['event'] == 'taskDeleted':
        delete_task(id)

    
    else:
        toke = UserInfo.objects.get(site_id = data["history_items"][0]["user"]["id"])
        token = toke.api_pk
        headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
        }
        r = requests.get(f"https://api.clickup.com/api/v2/task/{id}/?custom_task_ids=&team_id=&include_subtasks=", headers=headers)
        r = r.json()
        print(r)
        if data['event'] == 'taskCreated':
            if r["parent"] == None:
                create_task(r)
            else:
                create_sub_task(r)
        elif data['event'] == 'taskUpdated':
            if r["parent"] == None:
                update_task(r)
            else:
                update_sub_task(r)

        

def create_task(data):
    Task.objects.create(id = data["id"], name = data["name"], dscription = data["description"], status = data["status"]["status"], user = UserInfo.objects.get(site_id = data['creator']['id']))

def create_sub_task(data):
    try:
        p = Task.objects.get(id = data["parent"])
        SubTask.objects.create(id= data["id"], name= data["name"], description= data["description"], parent= p, user = UserInfo.objects.get(site_id = data['creator']['id']))
    except Task.DoesNotExist:
        print("object does not exist")

def update_task(data):
    try:
        time = int(data["time_spent"]/1000)  
        Task.objects.filter(id= data['id']).update(name = data["name"], dscription = data["description"], status = data["status"]["status"], hours= time)
    except:
        print('error object does not exist')

def update_sub_task(data):
    try: 
        SubTask.objects.filter(id= data['id']).update(name = data["name"], description = data["description"])
    except:
        print('error object does not exist')    

def delete_task(id):
    try:
        t = Task.objects.get(id=id)
        t.delete()
    except Task.DoesNotExist:
        try:
            tt = SubTask.objects.get(id=id)
            tt.delete()
        except SubTask.DoesNotExist:
            pass


