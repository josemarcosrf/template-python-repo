import os

from setuptools import find_packages
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

here = os.path.abspath(os.path.dirname(__file__))

# Avoids IDE errors, but actual version is read from version.py
__version__ = None
with open("my_package/version.py") as f:
    exec(f.read())

# Get the long description from the README file
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

tests_requires = [
    "pytest==5.1.3",
    "pytest-cov==2.7.1",
    "pytest-localserver==0.5.0",
    "pytest-sanic==1.0.0",
    "pytest-xdist==1.29.0",
    "responses==0.9.0",
    "freezegun==0.3.12",
    "nbsphinx==0.3.2",
    "aioresponses==0.6.0",
    "moto==1.3.8",
    "pluggy==0.13.1",
    "six==1.14.0",
    "coveralls==1.7.0",
]

dev_requires = [
    "black==19.10b0",
    "flake8==3.7.8",
    "pytype==2019.7.11",
    "pre-commit==1.21.0",
    "pre-commit-hooks==2.4.0",
]

install_requires = []

extras_requires = {
    "test": tests_requires,
    "dev": dev_requires,
}


class PostInstallCommand(install):
    """Custom install setup to help run shell commands
       (outside shell) after installation
    """

    def run(self):
        import subprocess

        subprocess.call(os.path.join(here, "scripts/dummy.sh"), shell=True)
        install.run(self)


class PostDevelopCommand(develop):
    """Custom install setup to help run shell commands
       (outside shell) after installation
    """

    def run(self):
        import subprocess

        subprocess.call(os.path.join(here, "scripts/dummy.sh"), shell=True)
        develop.run(self)


setup(
    cmdclass={"install": PostInstallCommand, "develop": PostDevelopCommand,},
    name="my_package",
    scripts=["scripts/dummy.sh"],
    dependency_links=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        # supported python versions
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.6",
    packages=find_packages(exclude=["tests", "tools", "docs", "contrib"]),
    entry_points={"console_scripts": []},
    version=__version__,
    install_requires=install_requires,
    tests_require=tests_requires,
    extras_require=extras_requires,
    include_package_data=True,
    description="Description of my_package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="MeliorAI Inc.",
    author_email="jose@melior.ai",
    maintainer="Jose Marcos Rodriguez",
    maintainer_email="jose@melior.ai",
    license="Apache 2.0",
    keywords="melior",
    url="https://melior.ai",
)

print("\nWelcome to Melior my_package!")
print("\nThis is my_package")
