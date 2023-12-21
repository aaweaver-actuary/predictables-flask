from setuptools import find_packages, setup

setup(
    name="predictables_flask",
    version="0.1",
    packages=find_packages(),
    # Add more parameters as needed
    install_requires=["flask", "flask_sqlalchemy"],
    entry_points={
        "console_scripts": [
            "predictables_flask=predictables_flask.cli:cli",
        ],
        "flask.commands": [
            "predictables_flask=predictables_flask.cli:cli",
        ],
        "flask.cli": [
            "predictables_flask=predictables_flask.cli:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    author="Predictables",
)
