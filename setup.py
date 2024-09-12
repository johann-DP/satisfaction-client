import subprocess
from setuptools import setup, find_packages

def install_requirements():
    try:
        subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'installation des dépendances : {e}")

install_requirements()

setup(
    name="Satisfaction Client",
    version="1.0",
    packages=find_packages(),
    install_requires=[],
    extras_require={
        'dev': [
            'black',
            'isort',
            'pylint'
        ]
    },
)
