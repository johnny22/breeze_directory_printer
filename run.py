""" This is the file to run to create a html directory ready for printing. """
from __future__ import print_function
import sys
import json
#import cPickle as pickle
import pickle
import breeze
import get_details
import family
import generate_template
import config



READ_FROM_DISK = config.READ_FROM_DISK
#WRITE = True
#ORDERED = True
FULL_PERSON_DICT = {}


def get_people_list():
    """One call"""

    try:
        print("Making first call ...")
        list_of_people = get_details.get_people_list()
        return list_of_people
    except breeze.breeze.BreezeError:
        print("Looks like there is a problem with your connection to breeze, check connect.py")
        raise breeze.breeze.BreezeError


def create_id_list(json_people):
    """No Calls"""
    out_list = []
    for person in json_people:
        out_list.append(person[u"id"])
    return out_list

def full_person_list(id_list):
    """one call per person in list"""
    out_list = []
    inc = 1
    for person_id in id_list:
        sys.stdout.write('\r')
        sys.stdout.flush()
        out_text = str("working on number " + str(inc) + " out of " + str(len(id_list)))
        sys.stdout.write(out_text)
        sys.stdout.flush()
        #print ("working on number ", inc, " out of ", len(id_list))
        try:
            person_details = get_details.get_person_details(person_id)
        except breeze.breeze.BreezeError:
            print("Looks like there is a problem with your connection to breeze, check connect.py")
            raise breeze.breeze.BreezeError
        out_list.append(person_details)
        FULL_PERSON_DICT[person_id] = person_details
        inc += 1
    sys.stdout.write('\n')
    return out_list


def get_family_list(list_of_people):
    """No Calls [('last_name', 'family_id', 'person_id'), ()].
     Here we are taking a list with all the info on everybody, and returning a
     list of tuples about the family
    """
    add = True
    out_list = []
    for person in list_of_people:
        in_booklet = is_in_booklet(person)

        # Three inclusion catagories: 1 = member, 2 = Attender, 47 = Non-communing Member
        if '1104100817' in person['details']:
            if person['details']['1104100817']['value'] in ('1', '2', '47') or in_booklet:
                if person['family'] == []:
                    family_id = None
                else:
                    family_id = person['family'][0]['family_id']

                for tup in out_list:
                    if person['family'] != []:
                        if tup[1] == person['family'][0]['family_id']:
                            add = False
                if add:
                    tuple_for_list = (person['last_name'],
                            family_id, person['id'])
                    out_list.append(tuple_for_list)
                    add = True
                else:
                    add = True
    return out_list

def is_in_booklet(person):
    """Checks for booklet tag"""
    in_booklet = False
    if '1954637534' in person['details']:
        if len(person['details']['1954637534']) > 1:
            if person['details']['1954637534'][1]['name'] == 'In':
                in_booklet = True
    return in_booklet

def family_object_list(in_family_list):
    """One call for each familiy, and one for each person in family. This function creates a list
    of all the people in a family."""
    out_list = []
    for family_tuple in in_family_list:
        family_json = FULL_PERSON_DICT[family_tuple[2]]
        for person in family_json['family']:
            if person['role_name'] == 'Head of Household':
                family_json = FULL_PERSON_DICT[person['person_id']]
        out_family = family.family_details(family_json, FULL_PERSON_DICT)
        out_list.append(out_family)
    out_list.sort(key=lambda person: person.last_name.lower())
    return out_list

def create_template_dict(obj_list):
    """No Calls. needs a list of 6 families. Should also be able to take less families."""
    while len(obj_list) < 6:
        obj_list.append(None)
    counter = 1
    out_dict = {}
    for obj in obj_list:
        var = "person" + str(counter)
        out_dict[var] = obj
        counter += 1
    return out_dict


def template_dict_caller(full_list):
    """No Calls"""
    number_of_dicts = len(full_list)/6
    if len(full_list)%6 == 0:
        add_var = 0
    else:
        add_var = 1
    out_list = []
    for temp_dict in range(0, number_of_dicts+add_var):
        out_list.append(create_template_dict(full_list[0:6]))
        full_list = full_list[6:]


    return out_list

def list_modifier(in_list):
    """No Calls"""
    out_list = []
    while len(in_list)%12 != 0:
        in_list.append(None)

    while in_list != []:
        out_list.append(in_list[-3:])
        in_list = in_list[:-3]
        out_list.append(in_list[:3])
        in_list = in_list[3:]
        out_list.append(in_list[:3])
        in_list = in_list[3:]
        out_list.append(in_list[-3:])
        in_list = in_list[:-3]

    final_out = [inner for outer in out_list for inner in outer]
    return final_out

if READ_FROM_DISK:
    print ("we are in reading from disk mode")
    try:
        with open('testing_dict_out.txt', 'r') as dict_in:
            FULL_PERSON_DICT = pickle.load(dict_in)
        with open('testing_out.json', 'r') as json_in:
            full_person_list = json.load(json_in)
    except IOError:
        print ("Looks like you need to run this with READ_TO_DISK = False, let me do that for you.""")
        READ_FROM_DISK = False

if not READ_FROM_DISK:
    people = get_people_list()
    list_of_ids = create_id_list(people)
    full_person_list = full_person_list(list_of_ids)
    with open('testing_out.json', 'w') as json_out:
        json.dump(full_person_list, json_out)
    with open('testing_dict_out.txt', 'w') as dict_out:
        dict_out.write(pickle.dumps(FULL_PERSON_DICT))




family_list = get_family_list(full_person_list)
object_list = family_object_list(family_list)


object_list = list_modifier(object_list)
sys.stdout.flush()
print(str(len(object_list)) + " entries in directory")

template_dict_list = template_dict_caller(object_list)
html_output = ''
for template_dict in template_dict_list:
    html_output += generate_template.render_template(**template_dict)
pre_info = ('<!DOCTYPE html> \n <html> \n <link rel="stylesheet" type="text/css"'
            ' href="./styles.css"> <body>')
post_info = '</body></html>'
final_output = pre_info + html_output + post_info
#if ORDERED:
with open('ordered_out.html', 'w') as out_html_file:
    out_html_file.write(final_output)


