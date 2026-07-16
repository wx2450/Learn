from setuptools import find_packages, setup

package_name = 'pj1_basics'

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
    maintainer='wx',
    maintainer_email='18159398990@163.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'minimal_node = pj1_basics.minimal_node:main',
            'message_publisher = pj1_basics.message_publisher:main',
            'message_subscriber = pj1_basics.message_subscriber:main',
            'virtual_arm = pj1_basics.virtual_arm:main',
            'joint_monitor = pj1_basics.joint_monitor:main',
        ],
    },
)
