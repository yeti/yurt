import os
from setuptools import setup, find_packages


def read(filepathname):
    with open(os.path.join(os.path.dirname(__file__), filepathname), 'r') as f:
        return f.read()


def get_package_data_files():
    package_data_files = ['django_project/ansible.cfg', 'django_project/.gitignore', 'requirements.txt']
    for orchestration, dirnames, filenames in os.walk('yurt/orchestration/'):
        for filename in filenames:
            package_data_files.append(os.path.join(orchestration.split('/', 1)[1], filename))
        for templates, dirnames, filenames in os.walk('yurt/templates/'):
            for filename in filenames:
                package_data_files.append(os.path.join(templates.split('/', 1)[1], filename))
    return package_data_files


long_description = "{}\n\n{}".format(read("README.rst"),
                                     read("CONTRIBUTORS.rst"))


setup(
    name="yak-yurt",
    packages=find_packages(),
    package_data={'yurt': get_package_data_files()},
    include_package_data=True,
    version="0.1.dev49",
    description="A tool for deploying Django Web Apps to remote servers",
    long_description=long_description,
    url="https://github.com/yeti/yurt/",
    license="MIT",
    author="Dean Mercado",
    author_email="support@yeti.co",
    install_requires=[
        "invoke==0.13.0",
        "ansible==2.1.0.0",
        "pycrypto==2.5",
        "click==6.6",
        "hvac==0.2.13"
    ],
    entry_points={
        "console_scripts": [
            "yurt=yurt.yurt_core.cli:main",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
