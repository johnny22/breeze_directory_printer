"""Gets list of all people details or a single persons details."""
from __future__ import print_function
import json
import connect

def get_people_list(tag=None, details=False):
    """Makes a request to breeze and returns list of all people."""
    if tag:
        #print (tag)
        people = connect.breeze_api.get_people(tag)
        return people

    else:
        #print (details)
        people = connect.breeze_api.get_people(details=True)
        #print (people)
        return people


def get_person_details(person_id):
    """Takes a persons id as input, makes a call to breeze,
    and returns a json of the persons details."""
    person = connect.breeze_api.get_person_details(person_id)
    return person

if __name__ == "__main__":
    PEOPLE_LIST = get_people_list(details=True)
    with open('people.json', 'w') as out_file:
        json.dump(PEOPLE_LIST, out_file)


