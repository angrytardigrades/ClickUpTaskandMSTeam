
#python3 code to get ClickUp task list and details
#command to run the code -> python3 ./get_tasks.py

# this is a python code to retrieve the task details from a specific List on ClickUp, 
# if you have the list ID then you can use this code to retrieve the task details
# and also if you are using "Team" you can use this  code to send Teams notification on team group, pretty cool 


import sys
import json
import requests   #this is for API
import pandas as pd
import pymsteams   #this library is for sending message on Microsoft Team (Webhook)
import numpy as np
import datetime
from msToDate import *
from DateToMS import *

current_date = datetime.now()
current_date_ms = Datetoms(current_date)
 
def get_tasks_details(clickup_api, list_id):
    try:
        url = "https://api.clickup.com/api/v2/list/%s/task?archived=false"%list_id  #this API is based on Clickup API v2.0 , if Clickup change or update the API then you need to check and update it if require
        headers = {"Authorization": clickup_api}
        r = requests.get(url = url, headers = headers)
        response_dict = json.loads(r.text)
        #print(response_dict)
 
        tasks = response_dict["tasks"]
        #print(tasks)
 
        clickup_tasks = pd.DataFrame()
        type(clickup_tasks)
        task_list = []
        for task in tasks:
            # the below list completely depends on the list of fields you have on your task list , you may need to remove or add fields here based on what you need
            tmp_dict = {}
            task_id = task['id']
            task_name = task['name']
            task_content = task['text_content']
 
            tmp_dict["task_name"] = task_name
            tmp_dict["task_id"] = task_id
            tmp_dict["task_content"] = task_content
 
            tmp_dict["date_created"] = task['date_created']
            tmp_dict["status"] = task['status']['status']
            tmp_dict["creator"] = task['creator']
            tmp_dict["assignees"] = task['assignees']
            tmp_dict["watchers"] = task['watchers']
            tmp_dict["due_date"] = task['due_date']
 
            #print("\n task name : %s | task id : %s "% (task_name, task_id))
 
            task_list.append(tmp_dict)
 
        clickup_tasks = pd.DataFrame.from_records(task_list)
        type(clickup_tasks)
 
        return clickup_tasks
 
    except:
        print("\n get_tasks_details Failed : ",sys.exc_info())
 

if __name__ == '__main__':
    try:
        print(" ClickUp task list and details process starts")
 
        clickup_api = " API KEY " # YOU NEED TO GET this Key from your ClickUp website ( your account ), google it and see where you can find it ( its under setting > app > API key)
        list_id = 210785740 # this is the list ID that you want to retrieve the task list , you can create a loop and run this code for multiple list , but API call is only for 1 list
 
        tasks_details_df = get_tasks_details(clickup_api, list_id)
        #silly part > here i had an issue that the output of my above function is noneType but i need PnadasDataframe to manipulate it , honestly i was lazy to check why its happening 
        #so i exported in CSV and then import in tasks_details_df_dataframe to make it PandaDataFrame :) easier but its not clean .. 
        # well you can improve this part :) let me know why the above function is not returning DataFrame
        tasks_details_df.to_csv("task.csv")
        tasks_details_df_dataframe = pd.read_csv("task.csv")

        #print(tasks_details_df)
        due_date_task = tasks_details_df_dataframe.dropna(subset=['due_date'])
        
        for i in range(len(due_date_task)):
            #you have the complete list of your tasks with all fields , from here its up to you what you want to do with these information
            # in below example , i select only those tasks that reached their Due date and then send each of them as a message on Team group...
            # BUT its totally up to you how to use the task infromations
            if (int(due_date_task.iloc[i,9]) - int(current_date_ms)<84400000) and due_date_task.iloc[i, 5]!="custom completed":
            
                myTeamsMessage = pymsteams.connectorcard("Put Team group Webhook here") #on team you need to create a Team , and then you have to install Webhook app and configure it for your Teams group at the end put the URL here
                # the below line is totaly depends on what you need from your task list ,here i picked "Task name " "Status " "Due date" ... but its up to you what field to use
                myTeamsMessage.text(str((due_date_task.iloc[i, 1],due_date_task.iloc[i, 5],due_date_task.iloc[i, 5], Mstodate(due_date_task.iloc[i, 9]))))
                myTeamsMessage.send()
        
        
        #for i in range(len(tasks_details_df))
 
        print("\n ClickUp task list and details process Finished.")
    except:
        print("\n ClickUp task list and details process Failed : ", sys.exc_info()) 

# Thanks to Jeevan Gupta!!