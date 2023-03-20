from setuptools import find_packages, setup

setup(
    name='world_spc',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-restful',
        'Flask-PyMongo',
        'python-dateutil',
        'marshmallow',
        'pymongo[srv]'
    ]
)
