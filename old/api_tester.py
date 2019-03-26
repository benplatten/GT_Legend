
from sitespeed_model import view_testURLs, Test

list_of_urls = ["https://www.waterwipes.com/uk/en"]

#dictionary of dictionaries 
# domain, url, device
#site_to_test[1]
# how is data recieved from model?


def site_speed_tool(site_to_test):

    import requests
    from requests.auth import HTTPBasicAuth
    import datetime
    import time
    import pandas as pd

    url = 'https://gtmetrix.com/api/0.1/test'
    location = '2' #London
    device = 'iphone_7' #or default
    payload = {"url":site_to_test,"location":location,"x-metrix-simulate-device":device}



    r = requests.post(url, data=payload,auth=HTTPBasicAuth('emarketing@reprisemedia.com', '7594ac5341cee9454564e0ba2d2a03d1'))

    post_response_data = r.json()
    print(post_response_data)

    state_url = post_response_data['poll_state_url']

    response_status = False

    while response_status == False:
        time.sleep(60)
        g = requests.get(state_url,auth=HTTPBasicAuth('emarketing@reprisemedia.com', '7594ac5341cee9454564e0ba2d2a03d1'))
        get_response_data = g.json()
        print(get_response_data['state'])

        if get_response_data['state'] == 'completed':
            response_status = True


    data = get_response_data
    print(data)


def gt_legend():
    #time control
    for i in list_of_urls:
        site_speed_tool(i)



gt_legend()