from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """Read the requirements from a file and return them as a list."""
    try:
        list_requirements:List[str] = []
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    list_requirements.append(requirement)
        
    except Exception as e:
        print(f"Error occurred while reading requirements: {e}")
    return list_requirements

setup(
    name='NetworkSecurity',
    version='0.0.1',
    author='Chethan D L',
    author_email='chethandl50@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements(),
)