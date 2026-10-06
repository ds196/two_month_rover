from setuptools import find_packages, setup

package_name = 'pico_relay'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='David Sharpe',
    maintainer_email='ds0196@uah.edu',
    description='Example serial relay for TM Rover',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "relay = pico_relay.relay_node:main"
        ],
    },
)
