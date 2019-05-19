import datetime
from flask import make_response, abort


def get_timestamp():
    return datetime.datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


USERS = {
    "Ivanov": {
        "fname": "Ivan",
        "lname": "Ivanov",
        "timestamp": get_timestamp(),
        "job": "MTS",
        "age": 33
    },
    "Petrov": {
        "fname": "Petr",
        "lname": "Petrov",
        "timestamp": get_timestamp(),
        "job": "Yandex",
        "age": 25
    },
    "Doe": {
        "fname": "John",
        "lname": "Doe",
        "timestamp": get_timestamp(),
        "job": "Luxoft",
        "age": 37
    }
}


def read_all():
    """
    This function responds to a request for /api_v1/users
    with the complete lists of users

    :return:        sorted list of users
    """
    return [USERS[key] for key in sorted(USERS.keys())]


def read_one(lname):
    """
    This function responds to a request for /api_v1/users/{lname}
    with one matching person from users
    :param lname:   last name of person to find
    :return:        person matching last name
    """
    if lname in USERS:
        person = USERS.get(lname)

    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )

    return person


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

    if lname not in USERS and lname is not None:
        USERS[lname] = {
            "lname": lname,
            "fname": fname,
            "timestamp": get_timestamp(),
            "age": age,
            "job": job,
        }
        return make_response(
            "{lname} successfully created".format(lname=lname), 201
        )

    else:
        abort(
            406,
            "Peron with last name {lname} already exists".format(lname=lname),
        )


def update(lname, person):
    """
    This function updates an existing person in the users structure
    :param lname:   last name of person to update in the users structure
    :param person:  person to update
    :return:        updated person structure
    """

    if lname in USERS:

        USERS[lname]["fname"] = person.get("fname")
        USERS[lname]["timestamp"] = get_timestamp()
        USERS[lname]["age"] = person.get("age")
        USERS[lname]["job"] = person.get("job")

        return USERS[lname]

    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )


def delete(lname):
    """
    This function deletes a person from the users structure
    :param lname:   last name of person to delete
    :return:        200 on successful delete, 404 if not found
    """

    if lname in USERS:
        del USERS[lname]
        return make_response(
            "{lname} successfully deleted".format(lname=lname), 200
        )

    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )
