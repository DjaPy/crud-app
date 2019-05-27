import datetime
from flask import make_response, abort
from flask_login import login_required

from config import db
from models import Person, PersonSchema


def get_timestamp():
    return datetime.datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


@login_required
def read_all():
    """
    This function responds to a request for /api_v1/users
    with the complete lists of users

    :return:        sorted list of users
    """
    users = Person.query.order_by(Person.lname).all()
    person_schema = PersonSchema(many=True)

    return person_schema.dump(users).data


@login_required
def read_one(person_id):
    """
    This function responds to a request for /api_v1/users/{lname}
    with one matching person from users
    :param person_id:   last name of person to find
    :return:        person matching last name
    """
    person = Person.query.filter(Person.id == person_id).one_or_none()
    if person:
        person_schema = PersonSchema()
        return person_schema.dump(person).data

    else:
        abort(
            404, "Person with last name {0} not found".format(person_id)
        )

    return person


@login_required
def create(person):
    """
    This function creates a new person in the users structure
    based on the passed in person data
    :param person:  person to create in users structure
    :return:        201 on success, 406 on person exists
    """
    lname = person.get("lname", None)
    fname = person.get("fname", None)
    age = person.get("age", None)
    job = person.get("job", None)

    existing_person = Person.query.filter(
        Person.fname == fname,
        Person.lname == lname,
        Person.age == age,
        Person.job == job
    ).one_or_none()

    if not existing_person:
        schema = PersonSchema()
        new_person = schema.load(person, session=db.session).data

        db.session.add(new_person)
        db.session.commit()

        return schema.dump(new_person).data, 201

    else:
        abort(
            406, "Person {lname} {fname} exists already".format(
                lname=lname, fname=fname
            )
        )


@login_required
def update(person_id, person):
    """
    This function updates an existing person in the users structure
    :param person_id:   last name of person to update in the users structure
    :param person:  person to update
    :return:        updated person structure
    """

    update_person = Person.query.filter(
        Person.id == person_id
    ).one_or_none()

    if update_person:
        schema = PersonSchema()
        update = schema.load(person, session=db.session).data

        update.id = update_person.id
        db.session.merge(update)
        db.session.commit()

        return schema.dump(update_person).data, 200

    else:
        abort(
            404, "Person not found for Id: {person_id} not found".format(
                person_id=person_id
            )
        )


@login_required
def delete(person_id):
    """
    This function deletes a person from the users structure
    :param person_id:   last name of person to delete
    :return:        200 on successful delete, 404 if not found
    """

    person = Person.query.filter(Person.id == person_id).one_or_none()

    if person:
        db.session.delete(person)
        db.session.commit()
        return make_response(
            "Person with Id: {person_id} deleted".format(person_id=person_id)
        )

    else:
        abort(
            404, "Person not found for Id: {person_id} not found".format(
                person_id=person_id
            )
        )
