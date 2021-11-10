from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from .models import List, Task, SubTask, UserInfo, Assignees, TimeTaskHistory, Space
from datetime import datetime, time



@api_view(['POST'])
def Clickup(request):
    if request.method == "POST":
        data = dict(request.data)
        print(data)
        request_router(data)
        return Response(status='200')



def request_router(data):
    if data["event"] == 'taskCreated' or data["event"] == 'taskUpdated' or data["event"] == 'taskDeleted':
        
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
    
    elif data["event"] == "taskTimeTrackedUpdated":
        toke = UserInfo.objects.get(site_id = data["history_items"][0]["user"]["id"])
        token = toke.api_pk
        task_id = data["task_id"]
        headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
        }
        r = requests.get(f'https://api.clickup.com/api/v2/task/{task_id}/time/?custom_task_ids=&team_id=', headers=headers)
        task_time_tracking(r.json(), toke.site_id, task_id)

    elif data["event"] == "spaceCreated" or data["event"] == "spaceUpdated" or data["event"] == "spaceDeleted":
        if data["event"] == "spaceDeleted":
            delete_space(data['space_id'])
        
        elif data["event"] == "spaceCreated":
            create_space(data)
        elif data["event"] == "spaceUpdated":
            update_space(data)
    
    elif data["event"] == "listCreated" or data["event"] == "listUpdated" or data["event"] == "listDeleted":
        if data["event"] == "listDeleted":
            delete_list(data)
        elif data["event"] == "listCreated":
            create_list(data)
        elif data["event"] == "listUpdated":
            update_list(data)



        


        

def create_task(data):
    t_est = 0 if data["time_estimate"] is None else data["time_estimate"]
    t_est = t_est / 3600000
    userr = UserInfo.objects.get(site_id = data['creator']['id'])
    task = Task.objects.create(id = data["id"], name = data["name"], dscription = data["description"], status = data["status"]["status"],
     user = userr,
     start_date = datetime.fromtimestamp(int(data["date_created"]) // 1000),
     time_estimate = t_est)
     
    for i in data["assignees"]:
        Assignees.objects.create(task = task, worker = UserInfo.objects.get(site_id = i['id']))


def create_sub_task(data):
    try:
        p = Task.objects.get(id = data["parent"])
        SubTask.objects.create(id= data["id"], name= data["name"], description= data["description"], parent= p, user = UserInfo.objects.get(site_id = data['creator']['id']))
    except Task.DoesNotExist:
        print("object does not exist")

def update_task(data):
    try:
        if data["date_closed"] != None:
            d_closed = datetime.fromtimestamp(int(data["date_closed"]) // 1000)
        else:
            d_closed = None
        t_est = 0 if data["time_estimate"] is None else data["time_estimate"]
        t_est = t_est / 3600000
        userr = UserInfo.objects.get(site_id = data['creator']['id'])
        time = int(data["time_spent"]/1000)  
        Task.objects.filter(id= data['id']).update(name = data["name"], dscription = data["description"], status = data["status"]["status"], hours= time, 
        end_date = d_closed, time_estimate = t_est)
        task = Task.objects.get(id = data['id'])
        

        a= []
        for i in data["assignees"]:
            a.append(i["id"])
        
        users = UserInfo.objects.filter(site_id__in=a)
        
        assig_to_delete = Assignees.objects.exclude(worker__in = a)
        assig_to_delete.delete()
        for user in users:
            p, created = Assignees.objects.get_or_create(worker = user, task = task)

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

def task_time_tracking(data, uid, taskid):
    user = UserInfo.objects.get(site_id = uid)
    headers = {
    'Authorization': user.api_pk,
    'Content-Type': 'application/json'
    }
    r = requests.get(f'https://api.clickup.com/api/v2/task/{taskid}/time/?custom_task_ids=&team_id=', headers=headers)
    r= r.json()
    for entry in r["data"]:
        if entry["user"]["id"] == uid:
            print(entry["intervals"][-1])
            time_data = entry["intervals"][-1]
            p, created =  TimeTaskHistory.objects.get_or_create(time_id = time_data["id"], started = datetime.fromtimestamp(int(time_data["start"]) // 1000),
            ended = datetime.fromtimestamp(int(time_data["end"]) // 1000),
            user= UserInfo.objects.get(site_id = uid),
            task = Task.objects.get(id = taskid),
            time = time_data["time"]//1000)


def create_space(data):
    try:
        user = UserInfo.objects.get(webhook_id = data["webhook_id"])
    except UserInfo.DoesNotExist:
        print("user does not exist info create space")
        return 0
    id = data["space_id"]

    headers = {
    'Authorization': user.api_pk
    }
    r = requests.get(f'https://api.clickup.com/api/v2/space/{id}', headers=headers)

    r = r.json()

    Space.objects.create(id = id, name = r["name"], private = r["private"], creator = user)

    

def update_space(data):
    try:
        user = UserInfo.objects.get(webhook_id = data["webhook_id"])
    except UserInfo.DoesNotExist:
        print("user does not exist info create space")
        return 0
    id = data["space_id"]

    headers = {
    'Authorization': user.api_pk
    }
    r = requests.get(f'https://api.clickup.com/api/v2/space/{id}', headers=headers)
    r = r.json()

    Space.objects.filter(id = id).update(name = r["name"], private = r["private"])

    

def delete_space(id):
    try:
        space = Space.objects.get(id = id)
    except Space.DoesNotExist:
        pass

def create_list(data):
    l_id = data["list_id"]
    user = UserInfo.objects.get(webhook_id = data["webhook_id"])

    headers = {
    'Authorization': user.api_pk
    }
    r = requests.get(f'https://api.clickup.com/api/v2/list/{l_id}', headers=headers)
    r= r.json()

    List.objects.create(id = l_id, name = r['name'], space = Space.objects.get(id= r['space']['id']))


def update_list(data):
    l_id = data["list_id"]
    user = UserInfo.objects.get(webhook_id = data["webhook_id"])

    headers = {
    'Authorization': user.api_pk
    }
    r = requests.get(f'https://api.clickup.com/api/v2/list/{l_id}', headers=headers)
    r= r.json()

    List.objects.filter(id = l_id).update(name = r['name'], space = Space.objects.get(id= r['space']['id']))

def delete_list(data):
    try:
        list = List.objects.get(id = data["list_id"])
        list.delete()
    except List.DoesNotExist:
        pass



