from setuptools import find_packages, setup

setup(
    name="predictables-flask",
    version="0.1",
    packages=find_packages(),
    install_requires=["flask", "flask_sqlalchemy"],
)
