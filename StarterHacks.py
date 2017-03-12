import collections
from uwaterlooapi import UWaterlooAPI
uw = UWaterlooAPI(api_key="938d42adae6cc93ed580450aef4cdbba")

# TAKES ABOUT 10 MINUTES TO RUN
# .txt files must be changed into appropriate .json files

big_list = uw.courses()
course_titles = {}
big_dict = {}
big_dict2 = {}



# A Course is a String

# A Prereq is one of:
# * list (Course)
# * listof (1, listof(Course))
# e.g. : ['MATH 106'] 
#        [1, 'CS115', 'CS135']
#        [[1, 'MATH235', 'MATH245'], [1, 'MATH237', 'MATH247']]



# Takes a list of prereqs and turns it into a listof (Course)
def filter_prereqs(lst):
    re = []
    if len(lst) > 0 and (lst[0] == 1 or lst[0] == 2 or lst[0] == 3):
        del lst[0]
        
    for i in lst:
        if isinstance(i,list):
            re.extend(filter_prereqs(i))
        else:
            re.append(i)
    return re


# Get the prereqs of a course as a list
def get_prereq (sub, cata):
    
    course = sub+cata
    
    raw_prereq = uw.course_prerequistes(sub,cata)
    
    # No prereqs for this course
    if (raw_prereq.get('prerequisites_parsed') == None or raw_prereq.get('prerequisites_parsed') == ''):
        return []
    
    big_dict2[course] = []
    big_dict2[course].append(uw.course(sub,cata)['prerequisites'])

    
    # Filter 1
    raw_prereq = raw_prereq['prerequisites_parsed']
    # Filter 2
    return filter_prereqs(raw_prereq)

    
# Produces a textfile with the every course which is a prereq, along with
#  an list of all courses it is a prereq of
def main ():

    # List of titles
    for course in big_list:
        course_titles[course['subject'] + course['catalog_number']] = course['title']

    # List of pre-reqs
    
    # List of post-reqs
    for course in big_list:
        
        sub = course['subject']
        cata = course['catalog_number']
        
        course = sub + cata + " - " + course_titles[sub+cata]
        list_of_prereqs = get_prereq(sub,cata)
        
        if (len(list_of_prereqs) != 0):
            
            for i in list_of_prereqs:

                # Not in the dictionary
                if big_dict.get(i) == None:
                    big_dict[i] = []
                    big_dict[i].append (course)
                else:
                    big_dict[i].append(course)
        

    o_big_dict = collections.OrderedDict(sorted((big_dict.items())))  
    print("Done!")
    f = open('post-requisites.txt', 'w')
    for key,value in o_big_dict.items():
        f.write("\"" + str(key) + "\": ")
        f.write(str(value)+",\n")
        f.close()


    o_big_dict2 = collections.OrderedDict(sorted((big_dict2.items())))
    print("Done!")
    f = open('pre-requisites.txt', 'w')
    for key,value in o_big_dict2.items():
        f.write("\"" + str(key) + "\": ")
        f.write(str(value)+",\n")
    f.close()
                

        
main()

