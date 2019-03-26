from flask import jsonify, Blueprint, abort

from flask_restful import (Resource, Api, reqparse,
                           inputs, fields, marshal,
                           marshal_with, url_for)

import models

test_fields = {
    'id': fields.Integer,
    "url" : fields.String,
    "test_date" : fields.DateTime,
    "onload_time" : fields.Integer,
    "first_contentful_paint_time" : fields.Integer,
    "report_url" : fields.Integer,
    "dom_interactive_time" : fields.Integer,
    "html_bytes" : fields.Integer,
    "fully_loaded_time" : fields.Integer,
    "html_load_time" : fields.Integer,
    "yslow_score" : fields.Integer,
    "pagespeed_score" : fields.Integer
}

def test_or_404(test_id):
    try:
        test = models.Test.get(models.Test.id==test_id)
    except models.Test.DoesNotExist:
        abort(404)
    else:
        return test
    

def add_url(test):
    Test.url = url_for('resources.Tests.Test', id=review.test.id)
    return Test

class Tests(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'url_id',
            required=True,
            type=inputs.positive,
            help='No client provided',
            location=['form','json']
        )
        self.reqparse.add_argument(
            'test_date',
            required=True,
            help='No test date provided',
            location=['form','json'],
            #type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S')
        )
        super().__init__()


    @marshal_with(test_fields)
    def get(self):
        return {'tests': [marshal(add_url(test),test_fields)
        for test in models.Test.select()
        ]}
    
    def post(self):
        args = self.reqparse.parse_args()
        models.Test.create(**args)
        return (add_url(test), 201, {
                'Location': url_for('resources.Tests.Test', id=Test.id)
               })


class Test(Resource):

    @marshal_with(test_fields)
    def get(self, id):
        return add_url(test_or_404(id))

    @marshal_with(test_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Tests.update(**args).where(models.Test.id==id)
        query.execute()
        return (add_url(models.Test.get(models.Test.id==id)), 200, 
            {'Location': url_for('resources.Tests.Test', id=id)})

    def delete(self, id):
        return jsonify({'url':'https://www.lv.com/car-insurance','test_date': '2019-03-01'})




tests_api = Blueprint('resources.tests', __name__)
api = Api(tests_api)
api.add_resource(
    Tests,
    '/tests',
    endpoint='tests'
    )
api.add_resource(
    Test,
    '/tests/<int:id>',
    endpoint='test'
    )