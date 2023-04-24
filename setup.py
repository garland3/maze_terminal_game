from setuptools import setup, find_packages

setup(
    name='mazegame',
    version='0.1',
    description='A package plays a CLI maze game',
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=[
        'dynaconf',
        'openai',
        'langchain',
        'numpy', 
    ],
    entry_points={
        'console_scripts': [
            'mazegame=mazegame.game:main',
        ],
    },
)
