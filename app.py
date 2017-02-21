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
