from chalice import Chalice, BadRequestError
from chalicelib import manage_graph
app = Chalice(app_name='coc-api')
app.debug = True

graph = manage_graph.initialize_db()
#graph = manage_graph.initialize_db()
@app.route('/')
def index():
    return "Conference of Champions API"

@app.route('/coc/api/v1.0/schedule/{attendee}')
def schedule(attendee):
    return manage_graph.get_json_attendee_schedule(attendee)


@app.route('/coc/api/v1.0/attendees')
def schedule():
    return manage_graph.get_json_attendees()

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.json_body
#     # Suppose we had some 'db' object that we used to
#     # read/write from our database.
#     # user_id = db.create_user(user_as_json)
#     return {'user_id': user_id}
#
# See the README documentation for more examples.
#
