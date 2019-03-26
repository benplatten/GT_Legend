
from sitespeed_model import view_testURLs, Test

dict_of_urls = view_testURLs()


def site_speed_tool(site_to_test,device_to_test,test_client):

    import requests
    from requests.auth import HTTPBasicAuth
    import datetime
    import time
    import pandas as pd

    client = test_client

    url = 'https://gtmetrix.com/api/0.1/test'
    location = '2' #London

    if device_to_test == 'mobile':
        payload = {"url":site_to_test,"location":location,"x-metrix-simulate-device":"iphone_7"}
    else:
        payload = {"url":site_to_test,"location":location}




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


    data = get_response_data["results"]
    data['url'] = site_to_test
    test_date = datetime.datetime.today().strftime('%Y-%m-%d')
    data['date'] = test_date
    data['device'] = device_to_test
    data['client'] = test_client


    url = data['url']
    test_date = data['date']
    onload_time = data['onload_time']
    first_contentful_paint_time = data['first_contentful_paint_time']
    report_url = data['report_url'] 
    dom_interactive_time = data['dom_interactive_time']
    html_bytes = data['html_bytes']
    fully_loaded_time = data['fully_loaded_time']
    html_load_time = data['html_load_time']
    yslow_score = data['yslow_score']
    pagespeed_score = data['pagespeed_score']
    device = data['device']
    client = data['client']





    print(data)
    try:
        Test.create(url=url, test_date=test_date,onload_time=onload_time,first_contentful_paint_time=first_contentful_paint_time,report_url=report_url,
                dom_interactive_time=dom_interactive_time,html_bytes=html_bytes,fully_loaded_time=fully_loaded_time,html_load_time=html_load_time,
                yslow_score=yslow_score,pagespeed_score=pagespeed_score,device=device,client=client
        )
        print("Test complete")

    except Exception as e: print(e)


def gt_legend():
    #time control
    for i in dict_of_urls:

        site_speed_tool(i['url'],i['device'],i['client'])



def time_test():
    from datetime import datetime
    from threading import Timer

    x=datetime.today()
    y=x.replace(day=x.day, hour=16, minute=0, second=0, microsecond=0)
    delta_t=y-x

    secs=delta_t.seconds+1

    def hello_world():
        print("hello world")
        #...

    t = Timer(secs, hello_world)
    t.start()

#time_test()

gt_legend()