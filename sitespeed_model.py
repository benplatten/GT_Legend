import datetime
import json
import re
import pandas as pd
import numpy as np

from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model


import plotly
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='Benjamin100', api_key='YjMKMZYiBw7Xx9gNmim0')



db = SqliteDatabase('sitespeed.db')


class TestURL(Model):
    client = CharField(max_length=255)
    url = CharField(max_length=255)
    device = CharField(max_length=255)
    test_key = CharField(max_length=255, unique=True)


    class Meta:
        database = db




class Test(Model):
    url = CharField(max_length=255)
    test_date = CharField(max_length=255)
    onload_time = IntegerField()
    first_contentful_paint_time = IntegerField()
    report_url = CharField(max_length=255)
    dom_interactive_time = IntegerField()
    html_bytes = IntegerField()
    fully_loaded_time = IntegerField()
    html_load_time = IntegerField()
    yslow_score = IntegerField()
    pagespeed_score = IntegerField()
    device = CharField(max_length=255)
    client = CharField(max_length=255)

    class Meta:
        database = db 



def purge():
    db.drop_tables([TestURL,Test])


### pass user input URLs to add_testURLs()
def add_testURLs(test_client,test_url,device_type):
    if device_type == "desktop_and_mobile":
        try:
            TestURL.create(client=test_client,url=test_url,device="mobile",test_key=test_url + "mobile")
            TestURL.create(client=test_client,url=test_url,device="desktop",test_key=test_url + "desktop")
            return '{} is now being tracked.'.format(test_url)
        except IntegrityError as e:
            return '{}'.format(e)
   
    else:
        try:
            TestURL.create(client=test_client,url=test_url,device=device_type,test_key=test_url + device_type)
            return '{} is now being tracked.'.format(test_url)
        except IntegrityError as e:
            return  '{}'.format(e)

            #{} is already being tracked.'.format(test_url)

            

### pass user input URLs to del_testURLs()
def del_testURLs(del_key):
        try: 
            TestURL.get(TestURL.test_key==del_key)
            d =TestURL.delete().where(TestURL.test_key==del_key)
            d.execute()
            return "{} is no longer being tracked.".format(del_key)
        except DoesNotExist:
            return "{} is not being tracked.".format(del_key)


def view_client_list():
    
    tracked_urls = []
    user_obj = TestURL.select(TestURL.client).distinct()

    for row in user_obj:
        json_data = json.dumps(model_to_dict(row))
        json_dict = json.loads(json_data)
        tracked_urls.append(json_dict)

    return tracked_urls



def view_testURLs():

    tracked_urls = []
    user_obj = TestURL.select()

    for row in user_obj:
        json_data = json.dumps(model_to_dict(row))
        json_dict = json.loads(json_data)
        tracked_urls.append(json_dict)

    return tracked_urls





### view gt_legend data
def view_URL_data(req_url):
    rows = []
    user_obj = Test.select().where(Test.url == req_url)
    #print(user_obj)
    for row in user_obj:
        json_data = json.dumps(model_to_dict(row))
        json_dict = json.loads(json_data)
        rows.append(json_dict)

    df1 = pd.DataFrame(rows)
    data1 = [
        go.Scatter(
            x=df1['test_date'], # assign x as the dataframe column 'x'
            y=df1['fully_loaded_time']
        )
    ]

    graphJSON1 = json.dumps(data1, cls=plotly.utils.PlotlyJSONEncoder)

    df2 = pd.DataFrame(rows)
    data2 = [
        go.Scatter(
            x=df2['test_date'], # assign x as the dataframe column 'x'
            y=df2['first_contentful_paint_time']
        )
    ]

    graphJSON2 = json.dumps(data2, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON1, graphJSON2 





def initialize():
    
    db.connect()
    db.create_tables([TestURL,Test], safe=True)


if __name__ == '__main__':
    initialize()
    add_testURLs()
    #del_testURLs()
    view_client_list()
    view_testURLs()
    view_URL_data()
    #purge()