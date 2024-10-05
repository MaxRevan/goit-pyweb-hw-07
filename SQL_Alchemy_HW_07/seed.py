import random
from db_config import Session
from models import Student, Group, Teacher, Subject, Grade
from faker import Faker

fake = Faker()

session = Session()

def create_groups():
    group_names = ['Group 113', 'Group 123', 'Group 133']
    for name in group_names:
        group = Group(name=name)
        session.add(group)
    session.commit()

def create_students():
    groups = session.query(Group).all()
    for _ in range(50):
        student = Student(
            fullname=fake.name(),
            group_id=random.choice(groups).id
        )          
        session.add(student)
    session.commit()

def create_teachers():
    for _ in range(5):
        teacher = Teacher(fullname=fake.name())
        session.add(teacher)
    session.commit()

def create_subjects():
    teacher_ids = [teacher.id for teacher in session.query(Teacher).all()] 
    subject_names = ['Math', 'Physics', 'Chemistry', 'History', 'Biology', 'Geography']
    for name in subject_names:
        subject = Subject(name=name, teacher_id=random.choice(teacher_ids))
        session.add(subject)
    session.commit()

def create_grades():
    student_ids = [student.id for student in session.query(Student).all()]
    subject_ids = [subject.id for subject in session.query(Subject).all()]
    for student_id in student_ids:
        for _ in range(random.randint(15, 20)):
            grade = Grade(
                student_id=student_id,
                subject_id=random.choice(subject_ids),
                grade=random.uniform(1, 10),
                date=fake.date_this_year()
            )
            session.add(grade)
    session.commit()


if __name__ == "__main__":
    create_groups()
    create_teachers()
    create_subjects()
    create_students()
    create_grades()