
from manage_graph import add_guest, add_person, add_event, add_participant, initialize_db
import json


def read_events_json():
    filename = "../event.json"
    with open(filename) as events_file:
        events_json = json.load(events_file)
        for event in events_json['events']:
            add_event(event)

def read_invitee_json():
    filename = "../load_person.json"
    with open(filename) as attendee_file:
        attendee_json = json.load(attendee_file)
        for invitee in attendee_json['attendees']:
            person = add_person(invitee)
            if 'guestOf' in invitee:
                add_guest(person, invitee['typeGuest'], invitee['guestOf'])


def read_attend_event_json():
    filename = "../attend_event.json"
    with open(filename) as scheduling_file:
        scheduling_json = json.load(scheduling_file)
        for participant in scheduling_json['schedulings']:
            add_participant(participant)

def main():
    initialize_db()
    read_invitee_json()
    read_events_json()
    read_attend_event_json()

# Start program
if __name__ == "__main__":
   main()
