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

def add_person(fname, mname, lname, typePerson):
    person = Person()
    person.fname = fname
    person.mname = mname
    person.lname = lname
    person.fullname = person.fname + person.mname + person.lname
    person.type = typePerson
    graph.push(person)
    return person


def add_event(event_json):
    event = Event()
    event.name = event_json['name']
    event.date = event_json['date']
    event.start_time = event_json['startTime']
    event.end_time = event_json['endTime']
    event.location = event_json['location']
    event.maximum_guests = event_json['maximumGuests']
    graph.push(event)


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



def add_participant(participant_json):
    #print(participant_json['attendeeName'] + " " + participant_json['eventName'])
    person = Person.select(graph, participant_json['attendeeName']).first()
    event = Event.select(graph, participant_json['eventName']).first()
    person.attending.add(event)
    graph.push(person)

def get_attendee_schedule(attendee):
    person = Person.select(graph, attendee).first()

    '''
    print("%s's schedule" % person.fullname)
    for event in person.attending:
        print("  %s" % event.name)
    '''
    return json.loads(person.fullname)

def get_json_attendee_schedule(attendee):
    return graph.data("MATCH (p:Person)-[:ATTENDING]->(e:Event) WHERE p.fullname = '%s' RETURN e.name as name" % attendee)

def get_json_attendees():
    return graph.data("MATCH (p:Person) RETURN p.fullname as fullname")

def main():
    #global graph
    #graph = Graph(password="hyenas")
    initialize_db()
    #read_invitee_json()
    #read_events_json()

    #read_attend_event_json()

    get_attendee_schedule('MarkWorkman')
    print('Attendees who are guests: ')
    for person in Person.select(graph).where("_.type = 'Guest'"):
        print("  " + person.fname + " " + person.lname)
    '''
    mark = Person()
    mark.fname = "Mark"
    mark.mname = ""
    mark.lname = "Workman"
    mark.fullname = mark.fname+mark.mname+mark.lname

    tina = Person()
    tina.fname = "Tina"
    tina.mname = "Marie"
    tina.lname = "Workman"
    tina.fullname = tina.fname + tina.mname + tina.lname

    mark.guest_of.add(tina, type="Spouse")

    awards = Event()
    awards.name = "Awards Banquet"
    awards.date = "6/10/2017"
    awards.startTime = "18:30"

    mark.attending.add(awards)
    tina.attending.add(awards)

    graph.push(tina)
    graph.push(mark)

    found = Person.select(graph, "TinaMarieWorkman").first()
    print(found.fname + " " + found.lname)

    for person in Person.select(graph).where("_.lname =~ 'W.*'"):
        print(person.fname + " " + person.lname)
    '''
# Start program
if __name__ == "__main__":
   main()
