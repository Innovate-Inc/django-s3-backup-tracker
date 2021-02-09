import os

from setuptools import find_packages, setup
#
# with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
#     README = readme.read()
#
# # allow setup.py to be run from any path
# os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name="django-s3_backup_tracker",
    version="0.0.1",
    author="Travis Bock",
    author_email="tbock@innovateteam.com",
    license="MIT",
    description="Move and track DB backups to offsite locations",
    url="https://github.com/Innovate-Inc/django-s3-backup-tracker",
    packages=['s3_backup_tracker', 's3_backup_tracker.migrations', 's3_backup_tracker.management.commands'],
    install_requires=['django-storages'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    include_package_data=True

)
