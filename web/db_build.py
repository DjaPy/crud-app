from config import db
from models import Person, Admin

USERS = [
    {
        "fname": "Ivan",
        "lname": "Ivanov",
        "job": "MTS",
        "age": 33,
    },
    {
        "fname": "Petr",
        "lname": "Petrov",
        "job": "Yandex",
        "age": 25,
    },
    {
        "fname": "John",
        "lname": "Doe",
        "job": "Luxoft",
        "age": 37,
    },
]

ADMIN = [
    {
        "login": "admin",
        "email": "admin@admin.ru",
        "password": "qwerty",
    }
]

db.create_all()

for person in USERS:
    person_instances = Person(
        lname=person.get('lname'),
        fname=person.get('fname'),
        age=person.get('age'),
        job=person.get('job')
    )

    db.session.add(person_instances)

for admin in ADMIN:
    admin_instance = Admin(
        login=admin.get('login'),
        email=admin.get('email'),
    )
    admin_instance.set_password(admin.get('password'))

    db.session.add(admin_instance)

db.session.commit()
