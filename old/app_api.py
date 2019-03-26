from flask import Flask, request
from flask import render_template



import models
from resources.site import urls_api
from resources.test import tests_api

urls_api

DEBUG = True
HOST = '127.0.0.1'
PORT = 5000


app = Flask(__name__)
app.register_blueprint(tests_api, url_prefix='/api/v1')


@app.route('/')
def hello_world():
	return render_template("index.html")


@app.route('/add', methods=['POST'])
def add_url():
	test_url_2 = request.form['test_url']
	test_name_2 = request.form['test_name']

	return (test_url_2, test_name_2)



if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG,host=HOST,port=PORT)

	## run gt_legend here?


