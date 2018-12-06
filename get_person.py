"""Makes a call to breeze and returns a person json."""
from __future__ import print_function
import json
import connect

def get_person_details(person_id):
    """Takes a persons id as input, makes a call to breeze,
    and returns a json of the persons details."""
    person = connect.breeze_api.get_person_details(person_id)
    return person

if __name__ == "__main__":
    INPUT_PERSON_ID = '8238427'
    OUT_PERSON = get_person_details(INPUT_PERSON_ID)
    with open('person.json', 'w') as out_file:
        json.dump(OUT_PERSON, out_file)
    #print json.dumps(person)


