def calculate_average(list):
    return sum(list)/len(list)

def mark_grade(average):
    if average >= 90:
        return 'A'
    elif average >= 80 and average < 90:
        return 'B'
    elif average >= 70 and average < 80:
        return 'C'
    elif average >= 60 and average < 70:
        return 'D'
    else:
        return 'F'
def process_grades(record: dict) -> dict:
    """
    input : list of records
    output : list of processed records

    records : {name and grade}


    Calculate average then mark the student based on the garde and add it to the record

    A: 90 <= average <= 100
    B: 80 <= average < 90
    C: 70 <= average < 80
    D: 60 <= average < 70
    F: average < 60
    """
    for dict in record:
        average = calculate_average(dict['grades'])
        dict['average'] = average
        dict['mark'] = mark_grade(average)

    return record


students = [ {'name': 'Alice', 'grades': [85, 92, 88]}, {'name': 'Bob', 'grades': [70, 75, 72]}, {'name': 'Charlie', 'grades': [50, 60, 58]}, {'name': 'David', 'grades': [95, 98, 100]} ]

print(process_grades(students))

