from sqlalchemy import func, desc
from db_config import Session
from models import Student, Group, Teacher, Subject, Grade

session = Session()


def select_1():
    results = session.query(
        Student.fullname, 
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    )\
    .select_from(Grade)\
    .join(Student)\
    .group_by(Student.id)\
    .order_by(desc('avg_grade'))\
    .limit(5)\
    .all()

    for fullname, avg_grade in results:
        print(f"Student: {fullname}, Average Grade: {avg_grade}")


def select_2():
    subjects = {1: "Math", 2: "Physics", 3: "Chemistry", 4: "History", 5: "Biology", 6: "Geography"}  
    print("Available subjects:")
    for id, subject in subjects.items():
        print(f"{id}: {subject}")
    subject_id = 3
    result = session.query(
        Student.fullname, 
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    )\
    .join(Grade).filter(Grade.subject_id == subject_id)\
    .group_by(Student.id)\
    .order_by(desc('avg_grade'))\
    .limit(1)\
    .one_or_none()

    if result:
        print(f"The student with the highest GPA in {subjects[subject_id]}: {result.fullname}, Average grade: {result.avg_grade}")
    else:
        print(f"No students found for {subjects[subject_id]}.")


def select_3():
    subject_id = 6
    result = session.query(
        Group.name.label('group_name'),
        Subject.name.label('subject_name'),
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    )\
    .join(Student, Group.id == Student.group_id)\
    .join(Grade, Student.id == Grade.student_id)\
    .join(Subject, Grade.subject_id == Subject.id)\
    .filter(Grade.subject_id == subject_id)\
    .group_by(Group.id, Subject.name)\
    .all()

    if result:
        print(f"Average grade for the subject '{result[0].subject_name}' in the groups:")
        for group_name, subject_name, average_grade in result:
            print(f"Group: {group_name}, Average grade: {average_grade:.2f}")
    else:
        print("No grades available for the specified subject.")


def select_4():
    result = session.query(
        func.round(func.avg(Grade.grade), 2).label('average_grade')
    ).scalar()

    if result is not None:
        print(f"Average grade: {result}")
    else:
        print("No grades found.")
    

def select_5():
    teacher_id = 1
    result = session.query(
        Teacher.fullname,
        Subject.name
    ).join(Subject).filter(Subject.teacher_id == teacher_id).all()

    if result:
        teacher_name = result[0].fullname
        print(f"Teacher: {teacher_name}")
        for _, subject_name in result:
            print(f"Subject: {subject_name}")
    else:
        print(f"No subjects found for teacher ID {teacher_id}.")


def select_6():
    group_name = "Group 113"
    result = session.query(
        Student.fullname
    )\
    .join(Group)\
    .filter(Group.name == group_name)\
    .all()

    if result:
        print(f"Students in {group_name}:")
        for student in result:
            print(student.fullname)


def select_7():
    group_name = "Group 123"
    subject_name = "Math"
    group = session.query(Group).filter(Group.name == group_name).first()
    subject = session.query(Subject).filter(Subject.name == subject_name).first()
    if group and subject:
        result = session.query(
            Student.fullname, Grade.grade
        )\
        .join(Grade)\
        .filter(
            Student.group_id == group.id,
            Grade.subject_id == subject.id
        )\
        .all()

        if result:
            print(f"Students in {group_name} with grades for {subject_name}:")
            for student_name, grade in result:
                print(f"{student_name}: {grade}")
    
    
def select_8():
    teacher_id = 1
    result = session.query(
        Teacher.fullname.label('teacher_name'),
        func.round(func.avg(Grade.grade), 2).label('average_grade')
    )\
    .join(Subject, Teacher.id == Subject.teacher_id)\
    .join(Grade, Subject.id == Grade.subject_id)\
    .filter(Teacher.id == teacher_id)\
    .group_by(Teacher.fullname)\
    .first()

    if result is not None:
        teacher_name, average_grade = result
        print(f"Average grade for {teacher_name}: {average_grade}")
    else:
        print(f"No grades found for {teacher_name}.")
    
        
def select_9():
    student_id = 34
    result = session.query(
        Student.fullname.label('student_name'),
        Subject.name.label('subject_name')
    )\
    .join(Grade, Student.id == Grade.student_id)\
    .join(Subject, Grade.subject_id == Subject.id)\
    .filter(Student.id == student_id)\
    .all()

    if result:
        print(f"Subjects for student {result[0].student_name}:")
        for _, subject_name in result:
            print(subject_name)
    else:
        print("No subjects for this student.")

def select_10():
    student_id = 13 
    teacher_id = 3 
    result = session.query(
        Student.fullname.label('student_name'),
        Subject.name.label('subject_name'),
        Teacher.fullname.label('teacher_name')
    )\
    .join(Grade, Student.id == Grade.student_id)\
    .join(Subject, Grade.subject_id == Subject.id)\
    .join(Teacher, Subject.teacher_id == Teacher.id)\
    .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)\
    .all()

    if result:
        print(f"Subjects for student {result[0].student_name} with teacher {result[0].teacher_name}:")
        for _, subject_name, _ in result:
            print(subject_name)
    else:
        print("No subjects for this student and teacher.")

def select_11():
    student_id = 47
    teacher_id = 1 
    result = session.query(
        Student.fullname.label('student_name'),
        Teacher.fullname.label('teacher_name'),
        func.avg(Grade.grade).label('average_grade')
    )\
    .join(Grade)\
    .join(Subject)\
    .join(Teacher)\
    .filter(
        Grade.student_id == student_id,
        Teacher.id == teacher_id
    )\
    .group_by(Student.fullname, Teacher.fullname)\
    .all()

    if result:
        for student_name, teacher_name, average_grade in result:
            print(f"Student: {student_name}, Teacher: {teacher_name}, Average grade: {average_grade:.2f}")
    else:
        print("No grades available for the specified student and teacher.")


def select_12():
    subject_id = 4
    group_id = 3
    result = session.query(
        Student.fullname.label('student_name'),
        Group.name.label('group_name'),
        Grade.grade,
        Subject.name.label('subject_name')
    )\
    .join(Grade, Student.id == Grade.student_id)\
    .join(Subject, Grade.subject_id == Subject.id)\
    .join(Group, Student.group_id == Group.id)\
    .filter(
        Student.group_id == group_id,
        Grade.subject_id == subject_id,
        Grade.date == (
            session.query(func.max(Grade.date))
            .filter(Grade.subject_id == subject_id,
                    Grade.student_id.in_(
                        session.query(Student.id).filter(Student.group_id == group_id)
                    ))
        )
    )\
    .all()
   
    if result:
        print(f"In the last lesson, the following grades were obtained:")
        for student_name, group_name, grade, subject_name in result:
            print(f"Group: {group_name}, Student: {student_name}, Grade: {grade}, Subject: {subject_name}")
    else:
        print("No grades available for the specified group and subject.")


def main():
    command = input("Enter a command: ")
    
    if command == "select_1":
        select_1()
    elif command == "select_2":
        select_2()
    elif command == "select_3":
        select_3()
    elif command == "select_4":
        select_4()
    elif command == "select_5":
        select_5()
    elif command == "select_6":
        select_6()
    elif command == "select_7":
        select_7()
    elif command == "select_8":
        select_8()
    elif command == "select_9":
        select_9()
    elif command == "select_10":
        select_10()
    elif command == "select_11":
        select_11()
    elif command == "select_12":
        select_12()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()