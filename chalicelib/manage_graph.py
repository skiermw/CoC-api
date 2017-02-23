#  manage_graph.py
import json
from py2neo import Graph, Node, Relationship
from py2neo.ext.calendar import GregorianCalendar
from py2neo.ogm import GraphObject,Property, RelatedFrom, RelatedTo
from CoC_Data_Model import Person, Event


#calendar = GregorianCalendar(graph)
def initialize_db():
    global graph
    graph = Graph(host="54.173.217.208", password="hyenas")
    return graph

def get_person(person_key):
    return Person.select(graph, '%s').first() %person_key

def add_person(person_json):
    person = Person()
    #  all attendees have these
    person.firstName = person_json['firstName']
    if 'middleName' in person_json:
        person.middleName = person_json['middleName']
    person.lastName = person_json['lastName']
    person.type = person_json['type']
    if 'preferredName' in person_json:
        person.preferredName = person_json['preferredName']
    if 'birthDate' in person_json:
        person.birthDate = person_json['birthDate']
    if 'cellPhone' in person_json:
        person.cellPhone = person_json['cellPhone']
    person.fullName = person.firstName + person.lastName
    #  Agent only
    if 'agentNumber' in person_json:
        person.agentNumber = person_json['agentNumber']
    #  Agent / DSM / RSM
    if 'stateNumber' in person_json:
        person.stateNumber = person_json['stateNumber']
        person.districtNumber = person_json['districtNumber']
    #  Officer
    if 'title' in person_json:
        person.title = person_json['title']
    if 'department' in person_json:
        person.department = person_json['department']
    #  Agent / DSM / RSM / Officer
    if 'city' in person_json:
        person.city = person_json['city']
        person.state = person_json['state']

    graph.push(person)
    return person

def add_guest(guest, type_guest, invitee_key):
    invitee = Person.select(graph, invitee_key).first()
    guest.guest_of.add(invitee, type=type_guest)
    graph.push(guest)
'''
def add_invitee(invitee_json):
    invitee_obj = add_person(invitee_json['firstName'],
                             invitee_json['middleName'],
                             invitee_json['lastName'],
                             invitee_json['type'])
    if 'guest' in invitee_json:
        guest_obj = add_person(invitee_json['guest']['firstName'],
                               invitee_json['guest']['middleName'],
                               invitee_json['guest']['lastName'], 'Guest')
        guest_obj.guest_of.add(invitee_obj, type=invitee_json['guest']['typeGuest'])
        graph.push(guest_obj)
'''


def add_participant(participant_json):
    print(participant_json['attendeeName'] + " " + participant_json['eventName'])
    person = Person.select(graph, participant_json['attendeeName']).first()
    event = Event.select(graph, participant_json['eventName']).first()
    person.attending.add(event)
    graph.push(person)

def add_event(event_json):
    event = Event()
    event.name = event_json['name']
    event.date = event_json['date']
    event.start_time = event_json['startTime']
    event.end_time = event_json['endTime']
    event.location = event_json['location']
    event.maximum_guests = event_json['maximumGuests']
    graph.push(event)

def get_attendee_schedule(attendee):
    person = Person.select(graph, attendee).first()
    return json.loads(person.fullname)

def get_json_attendee_schedule(attendee):
    return graph.data("MATCH (p:Person)-[:ATTENDING]->(e:Event) WHERE p.fullname = '%s' RETURN e.name as name, e.date as date, e.start_time as start_time, e.end_time as end_time, e.location as location order by e.date, e.start_time" % attendee)

def get_json_attendees():
    return graph.data("MATCH (p:Person) RETURN p.firstName as firstName,  p.lastName as lastName, p.type as type")

def main():
    #global graph
    #graph = Graph(password="hyenas")
    initialize_db()
    #read_invitee_json()
    read_events_json()

    #read_attend_event_json()

    #get_attendee_schedule('MarkWorkman')


# Start program
if __name__ == "__main__":
   main()
