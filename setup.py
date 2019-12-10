from setuptools import setup, find_packages

VERSION = "0.1"

setup(
    name="cdlapi",
    version=0.1,

    description="Python bindings for the Dota 2 match API",

    install_requires=[
        "requests"
        ,"gspread"
        ,"PyOpenSSL"
        ,"oauth2client"
        ,"lxml"
        ,"pymongo"
    ],
    entry_points={
    },
    zip_safe=False,
    include_package_data=True,
    package_data={
    },
    data_files=[
    ],

    keywords=[
    ],
    classifiers=[
    ],
)