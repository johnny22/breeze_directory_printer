"""Gets list of all people details."""
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

if __name__ == "__main__":
    PEOPLE_LIST = get_people_list(details=True)
    with open('people.json', 'w') as out_file:
        json.dump(PEOPLE_LIST, out_file)


