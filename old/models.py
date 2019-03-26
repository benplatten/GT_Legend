import datetime

from peewee import *

DATABASE = SqliteDatabase('speed.sqlite')


class TestList(Model):
	url = CharField(unique=True)
	test_name = CharField(unique=True)


class Test(Model):

	test_name = CharField(unique=True)
	url = ForeignKeyField(TestList, related_name='test_set')
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
	DATABASE.create_tables([TestList,Test], safe=True)
	DATABASE.close()