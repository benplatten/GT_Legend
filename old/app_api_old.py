from flask import Flask

import models
from resources.site import urls_api
from resources.test import tests_api

urls_api

DEBUG = True
HOST = '127.0.0.1'
PORT = 5000


app = Flask(__name__)
app.register_blueprint(urls_api, url_prefix='/api/v1')
app.register_blueprint(tests_api, url_prefix='/api/v1')


@app.route('/')
def hello_world():
	return 'Hello World'

	


if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG,host=HOST,port=PORT)

