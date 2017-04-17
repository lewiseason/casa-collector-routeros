from distutils.core import setup

setup(
    name='casa-collector-routeros',
    version='0.3.0',
    description='Collect information about RouterOS\'s ARP table and emit data and events to Redis',
    url='https://github.com/lewiseason/casa-collector-routeros',
    author='Lewis Eason',
    author_email='me@lewiseason.co.uk',
    packages = ['casa_collector_routeros'],
    install_requires=[
        'RouterOS-api',
        'redis',
        'apscheduler'
    ],
    entry_points={
        'console_scripts': [
            'casa-collector-routeros = casa_collector_routeros.collector:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3 :: Only'
    ]
)
