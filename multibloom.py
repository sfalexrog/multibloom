#!/usr/bin/env python

from __future__ import print_function
from catkin_pkg.topological_order import topological_order
import os
import subprocess
import shutil

ROS_VERSION = 'noetic'
PATH_PREFIX = os.path.abspath('') + '/src/'

def rosify(package_name):
    return ("ros-%s-" % ROS_VERSION) + package_name.replace("_", "-")

def generate_package(package):
    print("Generating rules for %s" % package[0])
    package_path = os.path.join(PATH_PREFIX, package[0])
    os.chdir(package_path)
    result = subprocess.call(['bloom-generate',
                              'rosdebian',
                              '--os-name',
                              'ubuntu',
                              '--os-version',
                              'focal',
                              '--ros-distro',
                              ROS_VERSION])
    print('Done; result is %d' % result)
    print('Creating package for %s' % package[0])
    result = subprocess.call(['fakeroot', 'debian/rules', 'binary'])
    print('Done; result is %d' % result)
    return result

def generate_rosdep(package_list):
    for package in package_list:
        rosified_name = rosify(package[1].name)
        yaml_content = """{}:
  ubuntu:
    focal: {}
""".format(package[1].name, rosified_name)

        with open('rosdep.yaml', 'a') as yaml_file:
            yaml_file.write(yaml_content)

def print_usage():
    print('Usage: multibloom.py rosdep | generate\n'
          'Verb meanings:\n'
          '  rosdep   - Generate a rosdep yaml file for\n'
          '             the packages in src\n'
          '  generate - Build .deb packages for all\n'
          '             packages in src\n')

if __name__ == '__main__':
    if len(os.sys.argv) < 2:
        print_usage()
        exit(1)
    packages = topological_order(PATH_PREFIX)
    if os.sys.argv[1] == 'rosdep':
        if not os.path.exists('rosdep.yaml'):
            generate_rosdep(packages)
            print("rosdep.yaml has been generated.")
        else:
            print("rosdep.yaml already exists.")
    elif os.sys.argv[1] == 'generate':
        for package in packages:
            generate_package(package)
        move_deb_files()
    else:
        print_usage()
        exit(1)
