from flask import jsonify, Blueprint, abort

from flask_restful import (Resource, Api, reqparse,
                           inputs, fields, marshal,
                           marshal_with, url_for)

import models

#used for marshal
url_fields = {
	'id': fields.Integer,
	'client': fields.String,
	'url': fields.String,
	'tests': fields.List(fields.String)
}

def add_tests(URL):
	URL.tests = [url_for('resources.tests.test', id=test.id) 
	             for test in URL.test_set]
	return test

def url_or_404(url_id):
	try:
		url = models.Site.get(models.Site.id==url_id)
	except models.Site.DoesNotExist:
		abort(404)
	else:
		return url



class URL_List(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'client',
			required=True,
			help='No client provided',
			location=['form','json']
			### 
		)
		self.reqparse.add_argument(
			'url',
			required=True,
			help='No URL name provided',
			location=['form','json'],
			type=inputs.url
		)
		super().__init__()

	@marshal_with(url_fields)
	def get(self):
		urls = [marshal(add_tests(url), url_fields) 
		        for url in models.Site.select()]
		return {'url_list':urls}

	@marshal_with(url_fields)
	def post(self):
		args = self.reqparse.parse_args()
		url = models.Site.create(**args)
		return (add_tests(url),201,{
			'Location': url_for('resources.Tests.Test', id=Test.id)
			})



class URL(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'client',
			required=True,
			help='No client provided',
			location=['form','json']
			### 
		)
		self.reqparse.add_argument(
			'url',
			required=True,
			help='No URL name provided',
			location=['form','json'],
			type=inputs.url
		)

		super().__init__()

	@marshal_with(url_fields)
	def get(self, id):
		return add_tests(url_or_404(id))

	@marshal_with(url_fields)
	def put(self, id):
		args = self.reqparse.parse_args()
		query = models.Site.update(**args).where(models.Site.id==id)
		query.execute()
		return (add_reviews(models.Course.get(models.Course.id==id)), 200,
            {'Location': url_for('resources.Sites.Site', id=id)})

	def delete(self, id):
		query = models.Site.delete().where(models.Site.id==id)
		query.execute()
		return ('', 204,
            {'Location': url_for('resources.Sites.Sites', id=id)})



urls_api = Blueprint('resources.urls', __name__)
api = Api(urls_api)
api.add_resource(
	URL_List,
	'/urls',
	endpoint='url_list'
	)
api.add_resource(
	URL,
	'/urls/<int:id>',
	endpoint='url'
	)