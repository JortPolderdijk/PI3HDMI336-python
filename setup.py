#!/user/bin/env python

from setuptools import setup, find_packages

import sys

setup(name		 = 'PI3HDMI336',
      version 		 = '1.0',
      author   		 = 'Jort Polderdijk',
      author_email 	 = 'j.polderdijk@student.fontys.nl',
      description	 = 'This is a library to control the PI3HDMI336 over I2C.',
      licence		 = 'MIT',
      url 		 = 'https://github.com/JortPolderdijk/PI3HDMI336-python',
      install_requires	 = ['Adafruit-GPIO'],
      packages 		 = find_packages());
