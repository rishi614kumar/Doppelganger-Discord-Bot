import pandas as pd
from datetime import datetime
import calendar
import time
import re
import sys
import string
import os

YOUR_JSONS= []
#selected discord usernames to alias dictionary. "discord_user#000" : "alias"
names_dict={}
#aliases of the people you want to pull. 'everyone' for everyone from the json file
names_list=['everyone']
#alias of the person you want to pull training text for. 'all' for everyone from the names_list
NAME = "all"
#will pull 1/LINK_FRACTION of all links. links affect training of the model significantly
LINK_FRACTION = 3
#destination file. rename to train.txt before using it with the model
DEST = "messages/"+NAME+"_messages.txt"


#concat the jsons
long_df = pd.read_json(YOUR_JSONS[0])
for i in range(1,len(YOUR_JSONS)):
    long_df=pd.concat([long_df,pd.read_json(YOUR_JSONS[i])])

df = new_df

#adjust the date field
new_dates=[]
days=[]
month_days=[]
times=[]
hours=[]
years=[]
for date in df['Date']:
    time_tuple = time.strptime(str(date)[0:19], "%Y-%m-%d %H:%M:%S")
    t = calendar.timegm(time_tuple)
    new_dates.append(time.ctime(t))
    days.append(str(time.ctime(t))[0:3])
    month_days.append(str(time.ctime(t))[4:10])
    times.append(str(time.ctime(t))[11:19])
    hours.append(str(time.ctime(t))[11:13])
    years.append(str(time.ctime(t))[20:24])
    
df['Date2']=new_dates
df['Day']=days
df['Month_day']=month_days
df['Time']=times
df['Hour']=hours
df['Year']=years

#adding the name field
names=[]
for user in df['User']:
    if user in names_dict.keys():
        names.append(names_dict[user])
    else:
        names.append("everyone")
df['Name']=names

#create a master json
df=df.reset_index()
df.to_json(r'master.json')

#cleaning the messsage text

#function to remove punctuation from messages
def clean(text):
    return re.sub(r'[^\w\s]','',text)


    
#messages from the json object cleaned and put into a text file
def messages_to_text(NAME,DEST,mdf):
    g = open(DEST, "w+",encoding="utf8")
    bad=['',' ','\n']
    link=0
    if NAME=='all':
        for message in mdf[mdf['Name'].isin(names_list)]['Message']:
            try:
                if not (message in bad):
                    cleaned_msg = message.encode("ascii", "ignore").decode()
                    if 'http' in cleaned_msg:
                        link=link+1
                        if link%LINK_FRACTION==0:
                            g.write(cleaned_msg+"\n")
                    else:
                        g.write(cleaned_msg+"\n")
            except:
                continue
    else:
        for message in mdf[mdf['Name']==NAME]['Message']:
            try:
                if not (message in bad):
                    cleaned_msg = message.encode("ascii", "ignore").decode()
                    if 'http' in cleaned_msg:
                        link=link+1
                        if link%LINK_FRACTION==0:
                            g.write(cleaned_msg+"\n")
                    else:
                        g.write(cleaned_msg+"\n")
            except:
                continue

    g.close()
    
#messages from the json object cleaned and put into a text file but with name labels
def messages_to_text_names(NAME,DEST,mdf):
    g = open(DEST, "w+",encoding="utf8")
    bad=['',' ','\n']
    link=0
    last_name=''
    if NAME=='all':
        df=mdf[mdf['Name'].isin(names_list)].drop(labels='level_0',axis=1).reset_index()
        for i in range(len(df)):
            message=df['Message'][i]
            boy_name=df['Name'][i]
            try:
                if not (message in bad):
                    cleaned_msg = message.encode("ascii", "ignore").decode()
                    send_msg = cleaned_msg+"\n"
                    if last_name!=boy_name:
                        last_name=boy_name
                        send_msg= '\n'+boy_name+":\n"+send_msg
                    if 'http' in cleaned_msg:
                        link=link+1
                        if link%LINK_FRACTION==0:
                            g.write(send_msg)
                    else:
                        g.write(send_msg)
            except:
                continue
    else:
        df=mdf[mdf['Name']==NAME].drop(labels='level_0',axis=1).reset_index()
        for i in range(len(df)):
            message=df['Message'][i]
            boy_name=df['Name'][i]
            try:
                if not (message in bad):
                    cleaned_msg = message.encode("ascii", "ignore").decode()
                    send_msg = cleaned_msg+"\n"
                    if last_name!=boy_name:
                        last_name=boy_name
                        send_msg= '\n'+boy_name+":\n"+send_msg
                    if 'http' in cleaned_msg:
                        link=link+1
                        if link%LINK_FRACTION==0:
                            g.write(send_msg)
                    else:
                        g.write(send_msg)
            except:
                continue

    g.close()

#creating the file
messages_to_text(NAME,DEST,df)

#creating the file but with name labels
#messages_to_text_names(NAME,DEST,df)


