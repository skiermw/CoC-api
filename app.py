from chalice import Chalice, BadRequestError, NotFoundError
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

@app.route('/coc/api/v1.0/attendees/{key}', methods=['GET', 'PUT'])
def attendee(key):
    request = app.current_request
    if request.method == 'PUT':
        return manage_graph.add_person(request.json_body)
    elif request.method == 'GET':
        try:
            return manage_graph.get_person(key)
        except KeyError:
            raise NotFoundError(key)

@app.route('/coc/api/v1.0/attendees')
def schedule():
    return manage_graph.get_json_attendees()
