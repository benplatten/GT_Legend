from flask import Flask, render_template, request

import sitespeed_model
from sitespeed_model import (add_testURLs, del_testURLs, view_testURLs,
                             view_URL_data,view_client_list
                             )

DEBUG = True
HOST = '127.0.0.1'
PORT = 5000

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")



@app.route('/add', methods=['POST'])
def add_url():
    test_url_parsed = request.form['test_url']
    client = request.form['test_client']
    device_type = request.form['device_type']
    data=add_testURLs(client,test_url_parsed,device_type)
    message = test_url_parsed + client + device_type
    return render_template('add.html',data=data)
    #('add.html', data=data)


@app.route('/delete', methods=['POST'])
def del_url():
    del_url_parsed = request.form['del_key']
    data=del_testURLs(del_url_parsed)
    return render_template('delete.html', data=data)

@app.route('/sitelist', methods=['POST'])
def view_urls():
    data=view_testURLs()
    return render_template('view_sitelist.html', data=data)


@app.route('/clientlist', methods=['POST'])
def view_clients():
    data=view_client_list()
    return render_template('view_clientlist.html', data=data)


@app.route('/url_data',methods=['POST'])
def request_view_URL_data():
    req_url = request.form['req_url']

    bar=view_URL_data(req_url)
    
    
    return render_template('view.html', plot=bar)




if __name__ == '__main__':
    sitespeed_model.initialize()
    
    app.run(debug=DEBUG,host=HOST,port=PORT)
