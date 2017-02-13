


from py2neo.ogm import GraphObject,Property, RelatedFrom, RelatedTo


class Person(GraphObject):
    'base OMG class for Person'
    __primarykey__ = "fullname"

    fname = Property()
    mname = Property()
    lname = Property()
    fullname = Property()
    type = Property()

    guest_of = RelatedTo("Person")
    guest = RelatedFrom("Person", "GUEST_OF")
    attending = RelatedTo("Event")


class Event(GraphObject):
    'base OMG class for Event'
    __primarykey__ = "name"

    name = Property()
    date = Property()
    start_time = Property()
    end_time_= Property()
    location = Property()
    maximum_guests = Property()

    attendees = RelatedFrom("Person", "ATTENDING")


