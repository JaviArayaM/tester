#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os 
from twilio.rest import Client
from twilio_config import TWILO_ACCOUNT_SID,TWILO_AUTH_TOKEN,PHONE_NUMBER,API_KEY_WAPI
import time

from requests import Request, Session 
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import pandas as pd
import requests 
from bs4 import BeautifulSoup
from tqdm import tqdm 

from datetime import datetime 


# # Armado url

# In[3]:


query="Santiago"
api_key=API_KEY_WAPI
url_clima="http://api.weatherapi.com/v1/forecast.json?key="+api_key+"&q="+query+"&days=1&aqi=no&alerts=no"


# In[5]:


response=requests.get(url_clima).json()


# In[6]:


response


# Una buena practica es cuando trabajamos con json es obtener las keys para navegarlo de manera más facil 

# In[7]:


response.keys()


# Ahora nos centraremos en el forecast y obtendremos sus keys 

# In[8]:


kforecast=response['forecast']['forecastday'][0].keys()
kforecast


# Nos centraremos en el campo hora, ya que es lo que le importa al usuario final

# In[9]:


len(response['forecast']['forecastday'][0]['hour'])


# Ahora tenemos que tener los datos especificos de uno de los registros

# In[10]:


response['forecast']['forecastday'][0]['hour'][1]['time'].split()[0] #fecha


# In[11]:


int(response['forecast']['forecastday'][0]['hour'][1]['time'].split()[1].split(':')[0]) #hora


# In[12]:


response['forecast']['forecastday'][0]['hour'][0]['condition']['text'] #condicion


# In[13]:


response['forecast']['forecastday'][0]['hour'][0]['temp_c'] #temp


# In[14]:


response['forecast']['forecastday'][0]['hour'][0]['will_it_rain']  #posibilidad de lluvia


# In[15]:


response['forecast']['forecastday'][0]['hour'][23]['chance_of_rain'] 


# In[ ]:





# # Crear data frame antes de hacer el envio al celu

# Haremos una funcion que extraiga los datos

# In[16]:


def get_forecast(response,i):
    fecha=response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]
    hora=int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    condicion=response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    temp=response['forecast']['forecastday'][0]['hour'][i]['temp_c']
    rain=response['forecast']['forecastday'][0]['hour'][i]['will_it_rain'] 
    probabilidad=response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain'] 
    
    return fecha, hora, condicion,temp,rain,probabilidad


# In[17]:


datos=[]

for i in tqdm(range(len(response['forecast']['forecastday'][0]['hour'])),colour='green'):
    datos.append(get_forecast(response,i))


# In[18]:


datos


# Ahora vamos a crear nuestro data frame 

# In[19]:


col=['fecha','hora','condicion','temp','rain','probabilidad']
df=pd.DataFrame(datos,columns=col)
df


# el usuario quiere obtener los dias con alta probabilidad de dlluvia, por lo que hay que filtrar 

# In[20]:


df_lluvia=df[(df['rain']==1) &(df['hora']>6) &(df['hora']<22)]
df_lluvia=df_lluvia[['hora','condicion']]
df_lluvia.set_index('hora',inplace=True)
df_lluvia


# In[21]:


PHONE_NUMBER


# In[25]:


import os
from twilio.rest import Client

account_sid = TWILO_ACCOUNT_SID
auth_token = TWILO_AUTH_TOKEN
client = Client(account_sid, auth_token)

message = client.messages.create(
                              body='Hola el pronostico de lluvia hoy es:  \n'+str(df_lluvia),
                              from_=PHONE_NUMBER,
                              to='+56979876440'
                          )

print(message.sid)


# In[ ]:





# In[ ]:




