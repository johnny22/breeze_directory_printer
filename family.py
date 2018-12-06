"""Creates family and person objects."""
from __future__ import print_function
import os
import json
#import get_person


class family_details(object):
    """ can I put all the info needed for display in here, or should this only
    contain general info and then link to other objects for the other people.
   """
    def __init__(self, in_json, in_dict):
        #member_list should be a list of person objects with specific data

        self.member_list = []
        self.in_json = in_json
        self.full_person_dict = in_dict
        self.image_folder = './Final_images'
        self.image_files = os.listdir(self.image_folder)
        #self.head_first_name = in_json['first_name']
        no_head_and_spouse = True
        # Currently adds head_first_name even if head isn't member,attender, or non-communing
        self.head_first_name = None
        for json_person in in_json['family']:
            if json_person['role_name'] == 'Head of Household':
                self.head_first_name = json_person['details']['first_name']
                no_head_and_spouse = False

        if in_json['family'] == []:
            self.head_first_name = in_json['first_name']
            self.add_member(in_json['id'])
            no_head_and_spouse = False

        if no_head_and_spouse:
            for json_person in in_json['family']:
                if json_person['role_name'] == 'Spouse':
                    self.head_first_name = json_person['details']['first_name']
        if not self.head_first_name:
            self.head_first_name = in_json['first_name']

        self.last_name = in_json['last_name']
        self.picture_path = "./Final_images/gray.png"
        self.get_all_members()
        self.get_picture_path()
        self.add_phone_number()
        self.add_address()
        #self.get_breeze_picture_path()
        self.order_member_list()
        self.different_names = False
        self.names()
        #print (self.__repr__(), ' ', self.last_name)


    def __repr__(self):
        output = []
        for member in self.member_list:
            output.append(str(member))
        return str(output)
    def add_address(self):
        """if address isn't private, and it exists, this will add it to the object."""
        display_address = True
        if '498938613' in self.in_json['details']:
            for address in self.in_json['details']['498938613']:
                if address['is_private'] == '1':
                    display_address = False
        if display_address:
            self.s_address = self.in_json['street_address']
            self.state = self.in_json['state']
            self.city = self.in_json['city']
            self.zipcode = self.in_json['zip']
        else:
            self.s_address = self.state = self.city = self.zipcode = None


    def add_phone_number(self):
        """If phone home phone number exists and isn't private, this will add it."""
        if '100604361' in self.in_json['details']:
            for number in self.in_json['details']['100604361']:
                if number['phone_type'] == 'home' and number['is_private'] == '0':
                    self.home_phone_number = number['phone_number']
        else:
            self.home_phone_number = None

    def add_member(self, new_member_id):
        """ adds tuple (personobj, ',' or '<br>) """
        #new_member = person(get_person.get_person_details(new_member_id))
        new_member = person(self.full_person_dict[new_member_id])
        if  new_member.role in ('1', '2', '47') or new_member.in_booklet:
            #self.member_list.append((new_member, var))
            self.member_list.append(new_member)

    def get_all_members(self):
        """Goes through family list and adds all members to the object."""
        add = True
        for member in self.in_json['family']:
            for included_person in self.member_list:
                if included_person.idnumber == member['person_id']:
                    add = False
            if add:
                self.add_member(member['person_id'])

    def get_picture_path(self):
        """Pretty sure this is what we are going to use, but I think it gets the picture path in some scenarios."""
        possible_list = []
        for picture in self.image_files:
            if self.last_name in picture:
                possible_list.append(picture)
        #print (possible_list)
        if len(possible_list) > 1:
            #if there are more than one family with the last name
            for pic in possible_list:
                if self.head_first_name in pic:
                    self.picture_path = self.image_folder + '/' + pic

        elif len(possible_list) == 1:
            pic_title = str(possible_list[0]).split('.')
            if self.head_first_name in possible_list[0]:
                #or ' ' not in possible_list[0]:
                self.picture_path = self.image_folder +'/' + possible_list[0]
            elif self.last_name == pic_title[0]:
                self.picture_path = self.image_folder +'/' + possible_list[0]
            #if ' ' in possible_list[0] and self.last_name == possible_list[0]:
            #    print( 'do we get here?')
            #    self.picture_path = self.image_folder + '/' + possible_list[0]
        else:
            #print ('len = 0', picture)
            self.picture_path = self.image_folder + '/gray.png'

        self.picture_path = self.picture_path.replace(' ', '%20')
        #print(self.picture_path)

    def get_breeze_picture_path(self):
        """Gets the picture path that breeze has, allowing you to download
        the picutres and then use them."""
        photo_name = str(self.head_first_name + '_' + self.last_name)
        #list_of_photos = []
        with open('photo_list.json', 'r') as in_photo:
            photo_json = json.load(in_photo)
            try:
                self.picture_path = photo_json[photo_name]
            except KeyError:
                print (photo_name, " Not in json")

    def order_member_list(self):
        """Sorts the member_list so that the children will be displayed in the proper order."""
        head_spouse_list = []
        children_with_grade = []
        children_no_grade = []
        for member in self.member_list:
            if not member.grade and member.family_role != 'Child':
                head_spouse_list.append(member)
            elif not member.grade and member.family_role == 'Child':
                children_no_grade.append(member)
            else:
                children_with_grade.append(member)
        children_with_grade.sort(key=lambda x: int(x.grade))
        head_spouse_list.extend(children_with_grade)
        head_spouse_list.extend(children_no_grade)
        self.member_list = head_spouse_list

    def names(self):
        """Defines attribute self.diferent_names if the spouses have different last names."""

        for member in self.member_list:
            if member.family_role == "Spouse" and member.last_name != self.last_name:
                self.different_names = True



class person(object):
    """Person Object."""
    def __init__(self, in_json):
        self.in_json = in_json
        self.var = ','
        self.idnumber = in_json['id']
        self.name = in_json['first_name']
        self.family_role = None
        self.assign_family_role()
        self.last_name = in_json['last_name']
        self.assign_email_address()
        self.assign_phone_number()
        self.assign_booklet_status()
        self.role = None
        self.assign_role()
        self.assign_grade()

    def assign_grade(self):
        """Assigns the grade based on in_json."""
        if 'grade' in self.in_json['details']:
            self.grade = self.in_json['details']['grade']
        else:
            self.grade = None

    def assign_booklet_status(self):
        """Checks the in_booklet tag and sets variable."""
        # is this redundant?
        self.in_booklet = False
        if '1954637534' in self.in_json['details']:
            if len(self.in_json['details']['1954637534']) > 1:
                if self.in_json['details']['1954637534'][1]['value'] == '72':
                    self.in_booklet = True

    def assign_role(self):
        """Assigns role based on in_json."""
        if '1104100817' in self.in_json['details']:
            self.role = self.in_json['details']['1104100817']['value']
        else:
            self.role = None

    def assign_phone_number(self):
        """Checks if phone number is private, and if it isn't, assigns the phone number."""
        if '100604361' in self.in_json['details']:
            for number in self.in_json['details']['100604361']:
                if number['phone_type'] == 'mobile' and number['is_private'] == '0':
                    self.phone_number = number['phone_number']
        else:
            self.phone_number = None

    def assign_email_address(self):
        """Assigns email address based on in_json."""
        if '1954637511' in self.in_json['details']:
            self.email = self.in_json['details']['1954637511'][0]['address']
        else:
            self.email = None

    def assign_family_role(self):
        """Assigns family role based on in_json."""
        if self.in_json['family'] != []:
            for member in self.in_json['family']:
                if member['person_id'] == self.idnumber:
                    self.family_role = member['role_name']
        else:
            self.familiy_role = None
        #print(self.family_role)


    def __repr__(self):
        return self.name





#def create_full_family_list(family_list):
#    """takes list [(lastname, family_id), ()] and creates family object.
#        I think should have head name and details, spouse name and details, and children
#        name(s) and details, address, last name, home phone. needs to have access to
#        full_list to search for everybody in the family. Each person in the family
#        has a bunch of info on everybdoy else, but I don't think it is enough all
#        by it self.
#        """
