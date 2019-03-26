import datetime

from peewee import *

DATABASE = SqliteDatabase('speed.sqlite')

class Site(Model):
	client = CharField()
	url = CharField(unique=True)
	## location + device


	class Meta:
		database = DATABASE

class Test(Model):

	
	url = ForeignKeyField(Site, related_name='test_set')
	test_date = DateTimeField()
	onload_time = IntegerField()
	first_contentful_paint_time = IntegerField()
	report_url = CharField(unique=True)
	dom_interactive_time = IntegerField()
	html_bytes = IntegerField()
	fully_loaded_time = IntegerField()
	html_load_time = IntegerField()
	yslow_score = IntegerField()
	pagespeed_score = IntegerField()

	class Meta:
		database = DATABASE


def initialize():
	"""create the database and tables if they don't exist."""
	DATABASE.connect()
	DATABASE.create_tables([Site,Test], safe=True)
	DATABASE.close()