
from setuptools import setup, find_packages

setup(
    name='assistants',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Add your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'prompt=assistants.cli.cli_prompt:run',
        ],
    },
)