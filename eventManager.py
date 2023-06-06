#### IMPORTS ####
import event_manager as EM


def validateId(student_id):
    return len(student_id) == 8 and student_id.isdigit() == True and student_id.startswith("0") == False

def validateName(student_name_list):
    for name in student_name_list:
        if name.isalpha() == False:
            return False
    return True

def validateAge(student_age, student_birth_year):
    return (int(student_age) in range(16,121)) and (2020 - int(student_age) == int(student_birth_year))

def validateSemester(student_semester):
    return int(student_semester)  > 0

def validateInput(lst):
    student_name_list = lst[1].split()
    return validateId(lst[0]) and validateName(student_name_list) and \
           validateAge(lst[2], lst[3]) and validateSemester(lst[4])

def normalizeString(str):
    return " ".join(str.split())

def normalizeInput(lst):
    for i in range(5):
        lst[i] = normalizeString(lst[i])
    pass

def readInput(input_file_path):
    file = open(input_file_path, 'r')
    input_list = []

    for line in file:
        input_line = []
        input_line = line.split(",")
        if len(input_line) == 5:
            normalizeInput(input_line)
            if validateInput(input_line) == True:
                removeOutdated(input_list, input_line[0])
                input_list.append(", ".join(input_line))
    

    file.close()
    return input_list

def removeOutdated(lst, student_id):
    for elem in lst:
        if elem.startswith(student_id):
            lst.remove(elem)
    pass

def writeOutput(output_file_path, lst):
    file = open(output_file_path, "w")
    for elem in lst:
        file.write(elem + "\n")
    
    file.close()
    pass

#### PART 1 ####
# Filters a file of students' subscription to specific event:
#   orig_file_path: The path to the unfiltered subscription file
#   filtered_file_path: The path to the new filtered file
def fileCorrect(orig_file_path: str, filtered_file_path: str):
    input_list = readInput(orig_file_path)
    input_list.sort()
    writeOutput(filtered_file_path, input_list)
    pass    


def sortStudentListByAge(lst):
    lst.sort()
    new_lst = []
    for age in range(16,121):
        for student in lst:
            if int(student.split(", ")[2]) == age:
                new_lst.append(student.split(", ")[1])
    return new_lst        

# Writes the names of the K youngest students which subscribed 
# to the event correctly.
#   in_file_path: The path to the unfiltered subscription file
#   out_file_path: file path of the output file
def printYoungestStudents(in_file_path: str, out_file_path: str, k: int) -> int:
    if k <= 0:
        return -1
    print_count = 0

    input_list = sortStudentListByAge(readInput(in_file_path))
    student_count = len(input_list)

    file = open(out_file_path, "w")
    for i in range(k):
        if i >= student_count:
            break
        file.write(input_list[i] + "\n")
        print_count += 1
    
    file.close()
    return print_count


    
# Calculates the avg age for a given semester
#   in_file_path: The path to the unfiltered subscription file
#   retuns the avg, else error codes defined.
def correctAgeAvg(in_file_path: str, semester: int) -> float:
    if semester < 1:
        return -1
    age_sum = 0
    student_count = 0
    input_list = readInput(in_file_path)

    for student in input_list:
        splited_student = student.split(", ")
        if int(splited_student[4]) == semester:
            student_count += 1
            age_sum += int(splited_student[2])
    if student_count > 0:
        return age_sum / student_count
    return 0
    
def getEarliestDate(dict_list):
    firstDict = dict_list[0]
    earliest_date = firstDict["date"]
    for event in dict_list:
        if EM.dateCompare(event["date"],earliest_date) <= 0:
            earliest_date = event["date"]
    return earliest_date

def fillEventManager(em, events):
    for event in events:
        EM.emAddEventByDate(em, event["name"], event["date"], event["id"])

#### PART 2 ####
# Use SWIG :)
# print the events in the list "events" using the functions from hw1
#   events: list of dictionaries
#   file_path: file path of the output file
def printEventsList(events :list,file_path :str):
    em = EM.createEventManager(getEarliestDate(events))
    fillEventManager(em, events)
    EM.emPrintAllEvents(em, file_path)
    return em
    
    
def testPrintEventsList(file_path :str):
    events_lists=[{"name":"New Year's Eve","id":1,"date": EM.dateCreate(30, 12, 2020)},\
                    {"name" : "annual Rock & Metal party","id":2,"date":  EM.dateCreate(21, 4, 2021)}, \
                                 {"name" : "Improv","id":3,"date": EM.dateCreate(13, 3, 2021)}, \
                                     {"name" : "Student Festival","id":4,"date": EM.dateCreate(13, 5, 2021)},    ]
    em = printEventsList(events_lists,file_path)
    for event in events_lists:
        EM.dateDestroy(event["date"])
    EM.destroyEventManager(em)

#### Main #### 
# feel free to add more tests and change that section. 
# sys.argv - list of the arguments passed to the python script
if __name__ == "__main__":
    import sys
    if len(sys.argv)>1:
        testPrintEventsList(sys.argv[1])