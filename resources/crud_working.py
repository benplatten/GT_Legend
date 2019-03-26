
def menu():
	if option_1:
		


def add_url():



def delete_url():
	# select a url


def view_url_data(test_name):
	data = Test.select().where(Test.test_name == test_name).order_by(Test.test_date.desc())
	# html form
	# action / button is a get request
	# url get parameters
	# route holds argument 
	# new route / page
	# turn this data into and SqLite query
	# return all data from database



@app.route('/new_test')
def new_test():
	#take url argument
	#add as site model
	return 'The following URL will be tracked {}'.format(new_test)

@app.route('/{}'.format(url_arg))
def view_url_data():






