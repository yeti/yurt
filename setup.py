import os
from setuptools import setup, find_packages


def read(filepathname):
    with open(os.path.join(os.path.dirname(__file__), filepathname), 'r') as f:
        return f.read()


long_description = "{0}\n".format(read("README.rst"))


setup(
    name="yak-yurt",
    packages=find_packages(),
    include_package_data=True,
    version="1.0.0",
    description="A tool for deploying Django Web Apps to remote servers",
    long_description=long_description,
    url="https://github.com/yeti/yurt/",
    license="MIT",
    author="Dean Mercado",
    author_email="support@yeti.co",
    test_suite="yurt.yurt_core.tests",
    setup_requires=[
        "click==6.6",
        "PyYAML==3.12",
        "cookiecutter==1.6.0",
        "invoke==1.1.0",
        "colorama==0.3.9"
    ],
    install_requires=[
        "click==6.6",
        "PyYAML==3.12",
        "cookiecutter==1.6.0",
        "invoke==1.1.0",
        "colorama==0.3.9"
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
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
