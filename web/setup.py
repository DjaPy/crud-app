from setuptools import setup, find_packages

install_requires = [
    'Flask==1.0.3',
    'Flask-SQLAlchemy==2.1',
    'psycopg2==2.8.2',
    'connexion[swagger-ui]',
    'Flask-Login',
    'flask-marshmallow',
    'marshmallow-sqlalchemy',
    'marshmallow==2.19.2',
    'flask-wtf',
    'gunicorn',
]

setup(
    name='RESTApi CRUD application',
    version='1.0',
    description='An example of a server designed to REST',
    platforms=['POSIX'],
    author="Sergey Ivanov",
    author_email="djapy@yandex.ru",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
)
